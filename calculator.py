"""
Calculator module: parsed activities + emission factors → total CO2 and breakdown.
No UI, no parsing; pure business logic.
"""

from typing import List

from emission_factors import get_food_factor, get_transport_factor
from models import (
    Activity,
    FoodActivity,
    TransportActivity,
    BreakdownItem,
    EmissionResult,
)


def calculate_emissions(activities: List[Activity]) -> EmissionResult:
    """
    Compute CO2 (kg) for each activity and total.
    Returns an EmissionResult with total_kg_co2 and breakdown list.
    """
    total = 0.0
    breakdown: List[BreakdownItem] = []

    for act in activities:
        if isinstance(act, FoodActivity):
            factor = get_food_factor(act.item)
            kg_co2 = act.quantity_kg * factor
            total += kg_co2
            breakdown.append(
                BreakdownItem(
                    description=f"Comida: {act.quantity_kg:.2f} kg de {act.item}",
                    kg_co2=round(kg_co2, 2),
                )
            )
        elif isinstance(act, TransportActivity):
            factor = get_transport_factor(act.mode)
            kg_co2 = act.distance_km * factor
            total += kg_co2
            breakdown.append(
                BreakdownItem(
                    description=f"Transporte: {act.distance_km:.1f} km en {act.mode}",
                    kg_co2=round(kg_co2, 2),
                )
            )

    return EmissionResult(
        total_kg_co2=round(total, 2),
        breakdown=breakdown,
    )
