"""
Emission factors for CO2 estimation.
Single source of truth: kg CO2 per unit (per kg food, per km transport, etc.).
Values are approximate and for prototyping; replace with authoritative sources for production.
"""

from typing import Dict, List

# --- Food (kg CO2 per kg of product, unless noted) ---
# Sources: simplified averages; real values vary by origin and production method.
FOOD_EMISSION_FACTORS: Dict[str, float] = {
    "carne": 27.0,           # beef, high impact
    "vacuno": 27.0,
    "res": 27.0,
    "cerdo": 6.5,
    "pollo": 6.0,
    "pescado": 5.0,
    "huevos": 4.5,
    "queso": 13.5,
    "leche": 1.3,
    "arroz": 4.0,
    "pasta": 1.5,
    "pan": 0.8,
    "verduras": 0.5,
    "frutas": 0.5,
    "legumbres": 1.0,
    "lentejas": 0.9,
    "tofu": 2.0,
    # English
    "meat": 27.0,
    "beef": 27.0,
    "pork": 6.5,
    "chicken": 6.0,
    "fish": 5.0,
    "eggs": 4.5,
    "cheese": 13.5,
    "milk": 1.3,
    "rice": 4.0,
    "vegetables": 0.5,
    "fruits": 0.5,
}

# Default portion size in kg when user doesn't specify quantity (e.g. "comí carne")
DEFAULT_FOOD_PORTION_KG: float = 0.15

# --- Transport (kg CO2 per passenger-km) ---
TRANSPORT_EMISSION_FACTORS: Dict[str, float] = {
    "bus": 0.089,
    "autobús": 0.089,
    "coche": 0.192,
    "carro": 0.192,
    "auto": 0.192,
    "moto": 0.113,
    "tren": 0.041,
    "metro": 0.041,
    "bici": 0.0,
    "bicicleta": 0.0,
    "pie": 0.0,
    "caminando": 0.0,
    # English
    "car": 0.192,
    "motorcycle": 0.113,
    "train": 0.041,
    "bike": 0.0,
    "bicycle": 0.0,
    "walking": 0.0,
    "foot": 0.0,
}

# --- Electricity (kg CO2 per kWh) - optional for "usé X horas de luz" ---
ELECTRICITY_EMISSION_FACTOR_KG_PER_KWH: float = 0.4  # grid average, region-dependent


def get_food_factor(food_key: str) -> float:
    """Return kg CO2 per kg for a food item, or 0 if unknown."""
    key = food_key.lower().strip()
    return FOOD_EMISSION_FACTORS.get(key, 0.0)


def get_transport_factor(transport_key: str) -> float:
    """Return kg CO2 per passenger-km for a transport mode."""
    key = transport_key.lower().strip()
    return TRANSPORT_EMISSION_FACTORS.get(key, 0.12)  # default ~average car


def get_default_food_portion_kg() -> float:
    return DEFAULT_FOOD_PORTION_KG


def list_food_keys() -> List[str]:
    """Return list of known food keys (for parser matching)."""
    return list(FOOD_EMISSION_FACTORS.keys())


def list_transport_keys() -> List[str]:
    """Return list of known transport keys (for parser matching)."""
    return list(TRANSPORT_EMISSION_FACTORS.keys())
