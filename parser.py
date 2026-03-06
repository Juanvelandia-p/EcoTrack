"""
Parser module: natural language text → structured activities.
Extracts food consumption and transport from Spanish/English sentences.
"""

import re
from typing import List, Optional, Set, Tuple

from emission_factors import (
    list_food_keys,
    list_transport_keys,
    DEFAULT_FOOD_PORTION_KG,
)
from models import FoodActivity, TransportActivity, Activity


# Patterns for transport: "20km en bus", "viajé 15 km en coche", "15 km by car"
TRANSPORT_PATTERNS = [
    re.compile(
        r"(?:viaj[eé]|recorrí|hice)\s+(\d+(?:[.,]\d+)?)\s*(?:km|kilómetros?)\s+(?:en|con)\s+(\w+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(?:km|kilómetros?)\s+(?:en|con)\s+(\w+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:traveled?|drove|rode)\s+(\d+(?:[.,]\d+)?)\s*(?:km|kilometers?)\s+(?:by|in)\s+(\w+)",
        re.IGNORECASE,
    ),
    re.compile(
        r"(\d+(?:[.,]\d+)?)\s*(?:km|kilometers?)\s+(?:by|in)\s+(\w+)",
        re.IGNORECASE,
    ),
]

FOOD_VERBS_ES = r"com[íi]|tom[eé]|desayun[eé]|almorz[eé]|cen[eé]|com[eé]"
FOOD_VERBS_EN = r"ate|eaten|had|drank"
FOOD_PATTERNS = [
    re.compile(
        rf"(?:{FOOD_VERBS_ES})\s+(\d+(?:[.,]\d+)?)\s*(g|kg|gramos?|kilos?)\s+(?:de\s+)?(\w+)",
        re.IGNORECASE,
    ),
    re.compile(
        rf"(?:{FOOD_VERBS_ES})\s+(\w+(?:\s+\w+)?)",
        re.IGNORECASE,
    ),
    re.compile(
        rf"(?:{FOOD_VERBS_EN})\s+(\d+(?:[.,]\d+)?)\s*(g|kg|grams?|kilos?)\s+(?:of\s+)?(\w+)",
        re.IGNORECASE,
    ),
    re.compile(
        rf"(?:{FOOD_VERBS_EN})\s+(\w+(?:\s+\w+)?)",
        re.IGNORECASE,
    ),
]


def _normalize_number(s: str) -> float:
    """Convert '1,5' or '1.5' to float."""
    return float(s.replace(",", "."))


def _parse_food_quantity(value: str, unit: str) -> float:
    """Convert value + unit to kg."""
    num = _normalize_number(value)
    u = unit.lower()
    if u in ("g", "gramo", "gramos", "grams"):
        return num / 1000.0
    return num


def _resolve_transport_mode(mode: str, transport_keys: List[str]) -> str:
    """Map raw match to a known transport key, or return normalized mode."""
    mode_lower = mode.lower()
    transport_set = {k.lower() for k in transport_keys}
    if mode_lower in transport_set:
        return mode_lower
    for tk in transport_keys:
        if tk.lower() in mode_lower or mode_lower in tk.lower():
            return tk.lower()
    return mode_lower


def _extract_transport(
    text: str, transport_keys: List[str]
) -> List[TransportActivity]:
    activities: List[TransportActivity] = []
    seen: Set[Tuple[float, str]] = set()

    for pattern in TRANSPORT_PATTERNS:
        for m in pattern.finditer(text):
            dist_str, mode = m.group(1), m.group(2)
            dist_km = _normalize_number(dist_str)
            mode = _resolve_transport_mode(mode, transport_keys)
            key = (dist_km, mode)
            if key in seen:
                continue
            seen.add(key)
            activities.append(
                TransportActivity(mode=mode, distance_km=dist_km)
            )
    return activities


def _resolve_food_item(food: str, food_set: Set[str]) -> Optional[str]:
    """Return matching food key if any, else None."""
    food_normalized = food.lower().strip().replace(" ", "")
    if food_normalized in food_set:
        return food_normalized
    for fk in food_set:
        if fk in food_normalized or food_normalized in fk:
            return fk
    return None


def _extract_food(text: str, food_keys: List[str]) -> List[FoodActivity]:
    activities: List[FoodActivity] = []
    food_set = {k.lower() for k in food_keys}
    seen: Set[Tuple[str, float]] = set()

    for pattern in FOOD_PATTERNS:
        for m in pattern.finditer(text):
            if len(m.groups()) == 3:
                value, unit, food = m.group(1), m.group(2), m.group(3)
                item = _resolve_food_item(food, food_set)
                if item is None:
                    continue
                kg = _parse_food_quantity(value, unit)
                key = (item, kg)
                if key in seen:
                    continue
                seen.add(key)
                activities.append(FoodActivity(item=item, quantity_kg=kg))
            else:
                food = m.group(1)
                item = _resolve_food_item(food, food_set)
                if item is None:
                    continue
                key = (item, DEFAULT_FOOD_PORTION_KG)
                if key in seen:
                    continue
                seen.add(key)
                activities.append(
                    FoodActivity(item=item, quantity_kg=DEFAULT_FOOD_PORTION_KG)
                )
    return activities


# Registry of extractors for scalability: add new functions here and call in parse_activities.
def _run_extractors(text: str) -> List[Activity]:
    """Run all activity extractors. Extend with new _extract_* and add here."""
    food_keys = list_food_keys()
    transport_keys = list_transport_keys()
    activities: List[Activity] = []
    activities.extend(_extract_transport(text, transport_keys))
    activities.extend(_extract_food(text, food_keys))
    return activities


def parse_activities(text: str) -> List[Activity]:
    """
    Parse natural language text and return a list of activities.
    Each activity is a FoodActivity or TransportActivity.
    """
    if not text or not text.strip():
        return []
    return _run_extractors(text.strip())
