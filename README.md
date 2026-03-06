# EcoTrack

Small prototype to estimate CO₂ footprint from a natural language description of daily activities.

## Run

From the **project root** (the `ecotrack` folder):

```powershell
pip install -r requirements.txt
python -m streamlit run app.py
```

## Example

Input: *"Hoy comí carne y viajé 20km en bus"*

- Food: carne (default portion) → ~4 kg CO₂  
- Transport: 20 km by bus → ~1.8 kg CO₂  
- **Total**: ~5.8 kg CO₂ (approximate)

## Project layout

- `app.py` – Streamlit UI (sidebar, examples, comparison)
- `config.py` – App config (defaults, decimals)
- `models.py` – Data types (FoodActivity, TransportActivity, EmissionResult)
- `emission_factors.py` – CO₂ factors (food, transport)
- `parser.py` – Text → list of activities
- `calculator.py` – Activities → total and breakdown
- `ARCHITECTURE.md` – Design and scalability notes

## Extending

- Add foods/transport in `emission_factors.py` and matching keywords in `parser.py`.
