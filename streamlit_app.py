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

    # -------------------------
    # pH ANALYSIS
    # -------------------------

    if ph < 6.5:

        issues.append(
            "pH is below the selected reference range."
        )

        recommendations.append(
            "Investigate possible acidic inputs or wastewater discharge."
        )

        prevention.extend([
            "Prevent untreated wastewater from entering the water body.",
            "Monitor nearby drainage and discharge points.",
            "Investigate possible acidic industrial or wastewater sources.",
            "Maintain regular pH monitoring to detect sudden changes."
        ])

    elif ph > 8.5:

        issues.append(
            "pH is above the selected reference range."
        )

        recommendations.append(
            "Investigate possible alkaline inputs or industrial discharge."
        )

        prevention.extend([
            "Prevent untreated alkaline wastewater from entering the water body.",
            "Monitor industrial and municipal discharge points.",
            "Investigate possible sources of alkaline contamination.",
            "Maintain regular pH monitoring to identify unusual changes."
        ])

    # -------------------------
    # TDS ANALYSIS
    # -------------------------

    if tds > 500:

        issues.append(
            "TDS is elevated."
        )

        recommendations.append(
            "Investigate possible dissolved substances and pollution sources."
        )

        prevention.extend([
            "Control wastewater and industrial discharge entering the water body.",
            "Investigate sources of dissolved salts or other substances.",
            "Monitor drainage outlets for unusual increases in TDS.",
            "Compare TDS readings over time to identify recurring pollution sources."
        ])

    # -------------------------
    # TURBIDITY ANALYSIS
    # -------------------------

    if turbidity > 5:

        issues.append(
            "Turbidity is elevated."
        )

        recommendations.append(
            "Investigate suspended solids, sediment, and possible contamination sources."
        )

        prevention.extend([
            "Reduce soil and sediment runoff into the water body.",
            "Control erosion around riverbanks and exposed soil.",
            "Prevent construction-site sediment from reaching the water.",
            "Maintain vegetation around vulnerable areas.",
            "Regularly monitor turbidity to identify recurring pollution events."
        ])

    # -------------------------
    # TEMPERATURE ANALYSIS
    # -------------------------

    if temperature > 35:

        issues.append(
            "Water temperature is relatively high."
        )

        recommendations.append(
            "Investigate possible thermal pollution or reduced water circulation."
        )

        prevention.extend([
            "Monitor sources of heated wastewater.",
            "Prevent excessively warm industrial discharge from entering the water body.",
            "Protect natural vegetation around the water body where appropriate.",
            "Continue temperature monitoring to identify unusual changes."
        ])

    # -------------------------
    # OVERALL RESULT
    # -------------------------

    st.header("📊 Water Quality Assessment")

    if len(issues) == 0:

        st.success(
            "✅ No major concerns detected from the selected parameters."
        )

    elif len(issues) <= 2:

        st.warning(
            "⚠️ Water-quality concerns detected."
        )

    else:

        st.error(
            "🚨 Multiple water-quality concerns detected."
        )

    # -------------------------
    # DETECTED CONDITIONS
    # -------------------------

    st.subheader("🔎 Detected Conditions")

    if issues:

        for issue in issues:
            st.write("• " + issue)

    else:

        st.write(
            "No major parameter concerns detected."
        )

    # -------------------------
    # RECOMMENDED ACTIONS
    # -------------------------

    st.subheader("🛠️ Recommended Actions")

    if recommendations:

        for recommendation in recommendations:
            st.write("• " + recommendation)

    else:

        st.write(
            "Continue regular monitoring and investigate the "
            "water body if other signs of pollution are observed."
        )

    # -------------------------
    # POLLUTION PREVENTION
    # -------------------------

    st.subheader("🌱 Pollution Prevention")

    if prevention:

        # Remove duplicate recommendations
        unique_prevention = list(dict.fromkeys(prevention))

        for item in unique_prevention:
            st.write("• " + item)

    else:

        st.write(
            "• Continue regular water-quality monitoring."
        )

        st.write(
            "• Prevent solid waste and untreated wastewater from entering the water body."
        )

        st.write(
            "• Maintain proper waste management around the water body."
        )

        st.write(
            "• Investigate sudden changes in water-quality measurements."
        )

    st.divider()

    st.caption(
        "Note: These recommendations are decision-support guidance. "
        "The four measured parameters alone cannot determine complete "
        "water safety or an exact chemical treatment process."
    )
