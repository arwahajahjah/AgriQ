import streamlit as st
import pandas as pd

from pipeline import run_pipeline

# =========================
# Page Config
# =========================
st.set_page_config(
    page_title="AgriQ Demo",
    layout="centered"
)

# =========================
# Title & Intro
# =========================
st.title("🌱 AgriQ – AI & Quantum-Inspired Agriculture")

st.markdown(
    """
    **AgriQ** is a decision engine that combines:
    - 🤖 **AI crop recommendation**
    - ⚛️ **Quantum-inspired optimization**

    to coordinate farmers under **water scarcity** and **market constraints**,
    preventing collective loss and price collapse.
    """
)

st.divider()

# =========================
# Number of Farmers
# =========================
st.header("👨‍🌾 Farmers Inputs")

num_farmers = st.selectbox(
    "Select number of farmers",
    options=[2, 3],
    key="num_farmers"
)

farmers_inputs = []

# =========================
# Farmer Input Forms
# =========================
for i in range(num_farmers):
    with st.expander(f"Farmer {i + 1}", expanded=True):

        N = st.slider("Nitrogen (N)", 0, 140, 90, key=f"N_{i}")
        P = st.slider("Phosphorus (P)", 0, 140, 40, key=f"P_{i}")
        K = st.slider("Potassium (K)", 0, 140, 40, key=f"K_{i}")

        temperature = st.slider("Temperature (°C)", 10, 40, 25, key=f"temp_{i}")
        humidity = st.slider("Humidity (%)", 20, 90, 65, key=f"hum_{i}")

        water_access = st.slider(
            "Water Access (0 = very limited)",
            0.0, 1.0, 0.5,
            key=f"water_{i}"
        )

        market_demand = st.slider(
            "Market Demand",
            0.0, 1.0, 0.8,
            key=f"market_{i}"
        )

        farming_type = st.selectbox(
            "Farming Type",
            options=[0, 1],
            format_func=lambda x: "Open Field" if x == 0 else "Greenhouse",
            key=f"type_{i}"
        )

        farmers_inputs.append({
            "N": N,
            "P": P,
            "K": K,
            "temperature": temperature,
            "humidity": humidity,
            "water_access": water_access,
            "market_demand": market_demand,
            "farming_type": farming_type
        })

st.divider()

# =========================
# System Constraints
# =========================
st.header("⚙️ System Constraints")

water_limit = st.slider(
    "Total Water Limit (shared across all farmers)",
    50, 300, 180,
    key="water_limit"
)

market_limit = {
    "orange": 1,
    "pigeonpeas": 2
}

st.caption(
    "Market constraint prevents over-production of the same crop."
)

st.divider()

# =========================
# Run Optimization
# =========================
if st.button("🚀 Run AgriQ Optimization", key="run_btn"):

    with st.spinner("Running AI + Quantum-Inspired Optimization..."):
        plan, score = run_pipeline(
            farmers_inputs=farmers_inputs,
            water_limit=water_limit,
            market_limit=market_limit
        )

    st.success("Optimization completed successfully ✅")

    # =========================
    # Results
    # =========================
    st.header("📊 Final Coordinated Planting Plan")

    df = pd.DataFrame(plan)
    st.dataframe(df, use_container_width=True)

    st.metric(
        label="Total System Profit Score",
        value=score
    )

    st.markdown(
        """
        **How to read the results**:
        - Each farmer receives **one coordinated crop decision**
        - The optimizer respects **water scarcity**
        - Market limits avoid **price collapse**
        - Profit is a **relative optimization score**, not accounting data
        """
    )

st.divider()

st.caption(
    "AgriQ – Prototype decision engine. UI layer demonstrated using Streamlit."
)

