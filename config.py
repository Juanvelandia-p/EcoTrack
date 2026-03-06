"""
App configuration and defaults.
Single place for tunable constants (locale, defaults, UI strings).
"""

# Default portion in kg when user does not specify quantity (e.g. "comí carne")
DEFAULT_FOOD_PORTION_KG: float = 0.15

# Display: decimal places for CO2 values
CO2_DECIMAL_PLACES: int = 2

# Comparison: kg CO2 per km for "equivalent to X km by car"
EQUIVALENT_CAR_KG_PER_KM: float = 0.192
