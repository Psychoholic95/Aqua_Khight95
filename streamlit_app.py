import streamlit as st
import requests

st.set_page_config(
    page_title="AquaGuard AI",
    page_icon="💧",
    layout="wide"
)

# ==========================================================
# LOGIN CONFIG
# (ESP32 firmware me AUTH_USER / AUTH_PASS SAME rakhna,
#  warna live-fetch fail ho jayega)
# ==========================================================

USERS = {
    "aquaguard": "12345678",
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================================================
# LOGIN SCREEN
# ==========================================================

def show_login():
    st.title("💧 AquaGuard AI")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("❌ Galat User ID ya Password.")


if not st.session_state.logged_in:
    show_login()
    st.stop()

# ==========================================================
# LOGGED IN -> DASHBOARD
# ==========================================================

with st.sidebar:
    st.write(f"👤 Logged in as **{st.session_state.username}**")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

st.title("💧 AquaGuard AI")
st.subheader("Smart Water Quality Analysis System")

st.write(
    "Sensor values manually daal sakte ho, ya niche ESP32 ka IP address "
    "daal kar seedha live reading fetch kar sakte ho."
)

# --------------------------------------------------
# LIVE FETCH FROM ESP32
# --------------------------------------------------

st.divider()
st.subheader("📡 Connect to ESP32 Sensor")

fcol1, fcol2 = st.columns([2, 1])

with fcol1:
    esp32_ip = st.text_input(
        "ESP32 IP Address",
        placeholder="e.g. 192.168.1.50",
        help="ESP32 ke Serial Monitor ya LCD par yeh IP dikhega jab wifi connect hoga."
    )

with fcol2:
    st.write("")
    st.write("")
    fetch_clicked = st.button("🔄 Fetch Live Data", use_container_width=True)

# Defaults, agar fetch se overwrite ho jayenge
if "temperature" not in st.session_state:
    st.session_state.temperature = 30.0
if "ph" not in st.session_state:
    st.session_state.ph = 7.0
if "tds" not in st.session_state:
    st.session_state.tds = 300.0
if "turbidity" not in st.session_state:
    st.session_state.turbidity = 5.0

if fetch_clicked:
    if not esp32_ip:
        st.warning("Pehle ESP32 ka IP address daalo.")
    else:
        try:
            url = f"http://{esp32_ip}/data"
            response = requests.get(
                url,
                auth=(st.session_state.username, USERS[st.session_state.username]),
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                st.session_state.ph = float(data.get("pH", st.session_state.ph))
                st.session_state.tds = float(data.get("tds", st.session_state.tds))
                st.session_state.turbidity = float(data.get("turbidity", st.session_state.turbidity))
                if not data.get("temp_error", False):
                    st.session_state.temperature = float(data.get("temperature", st.session_state.temperature))
                st.success("✅ Live data ESP32 se fetch ho gaya.")
            elif response.status_code == 401:
                st.error("❌ Authentication failed. ESP32 firmware ka user/pass check karo.")
            else:
                st.error(f"❌ ESP32 se error mila (status {response.status_code}).")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ ESP32 se connect nahi ho paya: {e}")

st.divider()

# --------------------------------------------------
# SENSOR INPUTS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    temperature = st.number_input(
        "🌡️ Temperature (°C)",
        value=st.session_state.temperature,
        key="temperature"
    )

with col2:
    ph = st.number_input(
        "🧪 pH",
        min_value=0.0,
        max_value=14.0,
        value=st.session_state.ph,
        key="ph"
    )

with col3:
    tds = st.number_input(
        "💧 TDS (ppm)",
        min_value=0.0,
        value=st.session_state.tds,
        key="tds"
    )

with col4:
    turbidity = st.number_input(
        "🌫️ Turbidity (NTU)",
        min_value=0.0,
        value=st.session_state.turbidity,
        key="turbidity"
    )

st.divider()

# --------------------------------------------------
# ANALYZE WATER
# --------------------------------------------------

if st.button("🔍 Analyze Water", use_container_width=True):

    issues = []
    recommendations = []
    prevention = []

    st.header("💧 Water Readings")

    st.write(f"**1. Temperature:** {temperature} °C")
    st.write(f"**2. pH:** {ph}")
    st.write(f"**3. TDS:** {tds} ppm")
    st.write(f"**4. Turbidity:** {turbidity} NTU")

    st.divider()

    # ---------------- pH ----------------
    if ph < 6.5:
        issues.append("pH is below the selected reference range.")
        recommendations.append("Investigate possible acidic inputs or wastewater discharge.")
        prevention.extend([
            "Prevent untreated wastewater from entering the water body.",
            "Monitor nearby drainage and discharge points.",
            "Investigate possible acidic industrial or wastewater sources.",
            "Maintain regular pH monitoring to detect sudden changes."
        ])
    elif ph > 8.5:
        issues.append("pH is above the selected reference range.")
        recommendations.append("Investigate possible alkaline inputs or industrial discharge.")
        prevention.extend([
            "Prevent untreated alkaline wastewater from entering the water body.",
            "Monitor industrial and municipal discharge points.",
            "Investigate possible sources of alkaline contamination.",
            "Maintain regular pH monitoring to identify unusual changes."
        ])

    # ---------------- TDS ----------------
    if tds > 500:
        issues.append("TDS is elevated.")
        recommendations.append("Investigate possible dissolved substances and pollution sources.")
        prevention.extend([
            "Control wastewater and industrial discharge entering the water body.",
            "Investigate sources of dissolved salts or other substances.",
            "Monitor drainage outlets for unusual increases in TDS.",
            "Compare TDS readings over time to identify recurring pollution sources."
        ])

    # ---------------- Turbidity ----------------
    if turbidity > 5:
        issues.append("Turbidity is elevated.")
        recommendations.append("Investigate suspended solids, sediment, and possible contamination sources.")
        prevention.extend([
            "Reduce soil and sediment runoff into the water body.",
            "Control erosion around riverbanks and exposed soil.",
            "Prevent construction-site sediment from reaching the water.",
            "Maintain vegetation around vulnerable areas.",
            "Regularly monitor turbidity to identify recurring pollution events."
        ])

    # ---------------- Temperature ----------------
    if temperature > 35:
        issues.append("Water temperature is relatively high.")
        recommendations.append("Investigate possible thermal pollution or reduced water circulation.")
        prevention.extend([
            "Monitor sources of heated wastewater.",
            "Prevent excessively warm industrial discharge from entering the water body.",
            "Protect natural vegetation around the water body where appropriate.",
            "Continue temperature monitoring to identify unusual changes."
        ])

    # ---------------- Overall assessment ----------------
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
            "Continue regular monitoring and investigate the "
            "water body if other signs of pollution are observed."
        )

    st.subheader("🌱 Pollution Prevention")
    if prevention:
        unique_prevention = list(dict.fromkeys(prevention))
        for item in unique_prevention:
            st.write("• " + item)
    else:
        st.write("• Continue regular water-quality monitoring.")
        st.write("• Prevent solid waste and untreated wastewater from entering the water body.")
        st.write("• Maintain proper waste management around the water body.")
        st.write("• Investigate sudden changes in water-quality measurements.")

    st.divider()
    st.caption(
        "Note: These recommendations are decision-support guidance. "
        "The four measured parameters alone cannot determine complete "
        "water safety or an exact chemical treatment process."
    )
