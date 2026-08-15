import streamlit as st

st.set_page_config(
    page_title="AquaGuard AI",
    page_icon="💧",
    layout="wide"
)

st.title("💧 AquaGuard AI")
st.subheader("Smart Water Quality Analysis System")

st.write(
    "Enter the water-quality readings below to analyze the "
    "condition of the water and receive recommendations."
)

# Sensor inputs
col1, col2, col3, col4 = st.columns(4)

with col1:
    temperature = st.number_input(
        "🌡️ Temperature (°C)",
        value=30.0
    )

with col2:
    ph = st.number_input(
        "🧪 pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0
    )

with col3:
    tds = st.number_input(
        "💧 TDS (ppm)",
        min_value=0.0,
        value=300.0
    )

with col4:
    turbidity = st.number_input(
        "🌫️ Turbidity (NTU)",
        min_value=0.0,
        value=5.0
    )

st.divider()

if st.button("🔍 Analyze Water", use_container_width=True):

    issues = []
    recommendations = []
    prevention = []

    # pH analysis
    if ph < 6.5:
        issues.append("pH is below the selected reference range.")
        recommendations.append(
            "Investigate possible acidic inputs or wastewater discharge."
        )
        prevention.append(
            "Monitor and control untreated wastewater entering the water body."
        )

    elif ph > 8.5:
        issues.append("pH is above the selected reference range.")
        recommendations.append(
            "Investigate possible alkaline inputs or industrial discharge."
        )
        prevention.append(
            "Monitor discharge sources and prevent untreated effluent from entering the water body."
        )

    # TDS analysis
    if tds > 500:
        issues.append("TDS is elevated.")
        recommendations.append(
            "Investigate possible dissolved substances and pollution sources."
        )
        prevention.append(
            "Control wastewater, industrial discharge, and polluted runoff."
        )

    # Turbidity analysis
    if turbidity > 5:
        issues.append("Turbidity is elevated.")
        recommendations.append(
            "Investigate suspended solids, sediment, and possible contamination sources."
        )
        prevention.append(
            "Reduce soil runoff and prevent waste and untreated discharge from entering the water body."
        )

    # Temperature
    if temperature > 35:
        issues.append("Water temperature is relatively high.")
        recommendations.append(
            "Investigate possible thermal pollution or reduced water circulation."
        )
        prevention.append(
            "Monitor sources of heated wastewater and protect natural water flow."
        )

    # Overall result
    st.header("📊 Water Quality Assessment")

    if len(issues) == 0:
        st.success("✅ No major concerns detected from the selected parameters.")
    elif len(issues) <= 2:
        st.warning("⚠️ Water-quality concerns detected.")
    else:
        st.error("🚨 Multiple water-quality concerns detected.")

    st.subheader("🔎 Detected Conditions")

    if issues:
        for issue in issues:
            st.write("• " + issue)
    else:
        st.write("No major parameter concerns detected.")

    st.subheader("🛠️ Recommended Actions")

    if recommendations:
        for recommendation in recommendations:
            st.write("• " + recommendation)
    else:
        st.write(
            "Continue regular monitoring and investigate the water body if other signs of pollution are observed."
        )

    st.subheader("🌱 Pollution Prevention")

    if prevention:
        for item in prevention:
            st.write("• " + item)
    else:
        st.write(
            "Continue regular monitoring, proper waste management, and prevention of untreated discharge."
        )

    st.divider()

    st.caption(
        "Note: These recommendations are decision-support guidance. "
        "The four measured parameters alone cannot determine complete water safety "
        "or an exact chemical treatment process."
    )
