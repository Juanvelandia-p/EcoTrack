# EcoTrack – Architecture

## Overview

EcoTrack estimates CO2 footprint from natural language descriptions of daily activities. The app is modular and separates concerns: emission data, parsing, calculation, config, and UI.

## Components

```
ecotrack/           # Project root – open this folder as workspace
├── app.py          # Streamlit UI entry point
├── config.py       # App config (defaults, decimals, comparison factor)
├── models.py       # Data types: FoodActivity, TransportActivity, EmissionResult
├── emission_factors.py  # CO2 factors (food, transport)
├── parser.py       # NLP / text → List[Activity]
├── calculator.py   # List[Activity] → EmissionResult
├── requirements.txt
└── ARCHITECTURE.md
```

## Data flow

1. **User input** → Free text (e.g. "Hoy comí carne y viajé 20km en bus").
2. **Parser** → Extracts activities as typed `FoodActivity` / `TransportActivity`.
3. **Calculator** → Uses `emission_factors` and returns `EmissionResult` (total + breakdown).
4. **UI** → Shows total, comparison (equivalent km by car), and per-activity breakdown.

## Module roles

| Module | Responsibility |
|--------|----------------|
| `models.py` | Dataclasses: `FoodActivity`, `TransportActivity`, `BreakdownItem`, `EmissionResult`. Single place for data shapes. |
| `config.py` | App-level constants: default portion, decimal places, comparison factor. |
| `emission_factors.py` | Kg CO2 per unit (food, transport). Single source of truth for factors. |
| `parser.py` | Regex/keyword extractors. Returns `List[Activity]`. Use `_run_extractors` to add new activity types. |
| `calculator.py` | Pure logic: `List[Activity]` → `EmissionResult`. No UI, no parsing. |
| `app.py` | Streamlit UI: input, sidebar (examples, tips), results, comparison. |

## Extensibility

- **New activities**: Add entries in `emission_factors.py` and a new `_extract_*` in `parser.py`; call it from `_run_extractors`.
- **New languages**: Add regex patterns in `parser.py`; factors stay the same.
- **New activity types** (e.g. electricity): Add a new dataclass in `models.py`, factor in `emission_factors.py`, extractor in `parser.py`, and branch in `calculator.calculate_emissions`.

## Scalability

- **Factors from file**: Replace in-memory dicts in `emission_factors.py` with loading from YAML/JSON or a DB for non-developer edits.
- **API layer**: `calculator.calculate_emissions` and `parser.parse_activities` are pure functions; wrap them in a FastAPI/Flask endpoint for a future API.
- **Caching**: Use `@st.cache_data` in the app for `parse_activities` / `calculate_emissions` if inputs grow or logic becomes heavier.
- **i18n**: Move UI strings from `app.py` into a config or locale files for multiple languages.
