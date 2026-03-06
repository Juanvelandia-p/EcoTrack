"""
Data models for EcoTrack.
Typed structures for activities and emission results to improve type safety and clarity.
"""

from dataclasses import dataclass
from typing import List, Union


@dataclass(frozen=True)
class FoodActivity:
    """A food consumption activity with item and quantity."""

    type: str = "food"
    item: str = ""
    quantity_kg: float = 0.0


@dataclass(frozen=True)
class TransportActivity:
    """A transport activity with mode and distance."""

    type: str = "transport"
    mode: str = ""
    distance_km: float = 0.0


Activity = Union[FoodActivity, TransportActivity]


@dataclass
class BreakdownItem:
    """Single line in the emission breakdown."""

    description: str
    kg_co2: float


@dataclass
class EmissionResult:
    """Result of CO2 calculation: total and per-activity breakdown."""

    total_kg_co2: float
    breakdown: List[BreakdownItem]
