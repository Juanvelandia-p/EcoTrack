"""
EcoTrack – Streamlit UI.
User enters a sentence; app parses activities, estimates CO2, and shows results.
"""

import streamlit as st

from config import CO2_DECIMAL_PLACES, EQUIVALENT_CAR_KG_PER_KM
from parser import parse_activities
from calculator import calculate_emissions
from models import FoodActivity, TransportActivity


# Custom CSS for a cleaner, distinctive look
PAGE_CSS = """
<style>
    /* Main container */
    .stApp { max-width: 720px; margin: 0 auto; }
    /* Hero section */
    .ecotrack-hero {
        padding: 1.5rem 0;
        border-bottom: 1px solid var(--border-color, #e0e0e0);
        margin-bottom: 1.5rem;
    }
    .ecotrack-hero h1 { font-size: 1.85rem; margin-bottom: 0.25rem; }
    .ecotrack-hero p { color: #5a5a5a; font-size: 0.95rem; }
    /* Result card */
    .ecotrack-result-card {
        background: linear-gradient(135deg, #e8f5e9 0%, #f1f8e9 100%);
        border: 1px solid #c8e6c9;
        border-radius: 12px;
        padding: 1.25rem 1.5rem;
        margin: 1rem 0;
    }
    .ecotrack-total { font-size: 1.75rem; font-weight: 700; color: #2e7d32; }
    .ecotrack-comparison { font-size: 0.9rem; color: #558b2f; margin-top: 0.5rem; }
    /* Breakdown list */
    .ecotrack-breakdown-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0.75rem;
        margin: 0.25rem 0;
        background: #fafafa;
        border-radius: 8px;
        border-left: 4px solid #81c784;
    }
    .ecotrack-breakdown-desc { font-weight: 500; }
    .ecotrack-breakdown-co2 { color: #2e7d32; font-weight: 600; }
    /* Sidebar */
    .ecotrack-sidebar-section { margin-bottom: 1.25rem; }
    .ecotrack-sidebar-section h3 { font-size: 0.9rem; color: #666; margin-bottom: 0.5rem; }
    .ecotrack-example {
        padding: 0.5rem 0.6rem;
        background: #f5f5f5;
        border-radius: 6px;
        font-size: 0.85rem;
        margin: 0.35rem 0;
        cursor: pointer;
    }
    .ecotrack-example:hover { background: #eeeeee; }
    .ecotrack-disclaimer { font-size: 0.75rem; color: #888; margin-top: 1rem; }
</style>
"""


def _format_activity(act) -> str:
    """Human-readable one-line description of an activity."""
    if isinstance(act, FoodActivity):
        return f"Comida: {act.quantity_kg:.2f} kg de {act.item}"
    if isinstance(act, TransportActivity):
        return f"Transporte: {act.distance_km:.1f} km en {act.mode}"
    return str(act)


def _equivalent_km_car(kg_co2: float) -> float:
    """Convert kg CO2 to equivalent km by car for comparison."""
    if EQUIVALENT_CAR_KG_PER_KM <= 0:
        return 0.0
    return kg_co2 / EQUIVALENT_CAR_KG_PER_KM


def render_sidebar() -> None:
    """Sidebar with examples and tips."""
    with st.sidebar:
        st.markdown("### Cómo usar")
        st.markdown(
            "Escribe en español o inglés. Incluye **comidas** (ej: comí pollo, 200g de arroz) "
            "y **desplazamientos** (ej: 15 km en coche, 20 km by bus)."
        )

        st.markdown("---")
        st.markdown("**Ejemplos**")
        examples = [
            "Hoy comí carne y viajé 20 km en bus.",
            "Desayuné pan y café. 10 km en coche.",
            "Ate 150g of beef. Traveled 5 km by bike.",
        ]
        for ex in examples:
            if st.button(ex, key=f"ex_{hash(ex) % 10**8}", use_container_width=True):
                st.session_state["ecotrack_input"] = ex
                st.rerun()

        st.markdown("---")
        st.markdown("**Alimentos** reconocidos: carne, pollo, pescado, arroz, pan, verduras, etc.")
        st.markdown("**Transporte**: bus, coche, tren, bici, metro, moto.")

        st.markdown("---")
        st.caption(
            "EcoTrack es un prototipo. Los factores de emisión son aproximados y orientativos."
        )


def main() -> None:
    st.set_page_config(
        page_title="EcoTrack",
        page_icon="🌱",
        layout="centered",
        initial_sidebar_state="expanded",
    )
    st.markdown(PAGE_CSS, unsafe_allow_html=True)

    # Sidebar
    render_sidebar()

    # Hero
    st.markdown(
        '<div class="ecotrack-hero">'
        "<h1>🌱 EcoTrack</h1>"
        "<p>Describe tus actividades del día y estima tu huella de CO₂.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

    text = st.text_area(
        "¿Qué hiciste hoy?",
        placeholder="Ej: Hoy comí carne y viajé 20 km en bus. También desayuné pan.",
        height=120,
        help="Escribe en español o inglés. Incluye comidas y desplazamientos.",
        label_visibility="visible",
        key="ecotrack_input",
    )

    if st.button("Calcular huella de CO₂", type="primary", use_container_width=True):
        if not text or not text.strip():
            st.warning("Escribe al menos una actividad.")
            return

        activities = parse_activities(text)
        if not activities:
            st.info(
                "No se detectaron actividades conocidas. Prueba con frases como: "
                "«comí carne», «viajé 10 km en bus»."
            )
            return

        result = calculate_emissions(activities)

        # Detected activities (transparency)
        with st.expander("Actividades detectadas", expanded=False):
            for act in activities:
                st.markdown(f"- {_format_activity(act)}")

        # Total and comparison
        total = result.total_kg_co2
        equiv_km = _equivalent_km_car(total)
        st.markdown(
            f'<div class="ecotrack-result-card">'
            f'<div class="ecotrack-total">{total:.{CO2_DECIMAL_PLACES}f} kg CO₂</div>'
            f'<div class="ecotrack-comparison">'
            f'Aproximadamente equivalente a {equiv_km:.0f} km en coche.'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        # Breakdown
        st.subheader("Desglose")
        for item in result.breakdown:
            st.markdown(
                f'<div class="ecotrack-breakdown-item">'
                f'<span class="ecotrack-breakdown-desc">{item.description}</span>'
                f'<span class="ecotrack-breakdown-co2">{item.kg_co2} kg CO₂</span>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.caption(
            "Valores aproximados para uso orientativo. Factores por defecto para alimentos y transporte."
        )


if __name__ == "__main__":
    main()
