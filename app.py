import streamlit as st

# ✅ MUST BE FIRST COMMAND
st.set_page_config(
    page_title="HealthSync AI",
    layout="wide",
    page_icon="🏥"
)

# ------------------- IMPORT PAGES -------------------
from my_pages import (
    dashboard,
    patient_details,
    live_monitoring,
    risk_analysis,
    reports,
    alerts,
    trend_analysis,
    treatment_plan
)

# ------------------- SESSION STATE INIT -------------------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ------------------- THEME -------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #dff5ea, #c7e9d7);
}

.card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.title {
    font-size: 32px;
    font-weight: bold;
    color: #065f46;
}

.stButton > button {
    background-color: #22c55e;
    color: white;
    border-radius: 10px;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# ------------------- SIDEBAR -------------------
st.sidebar.markdown("## 🏥 HealthSync AI")


# ------------------- NAVIGATION -------------------
pages = [
    "Dashboard",
    "Patient Details",
    "Live Monitoring",
    "Trend Analysis",
    "Risk Analysis",
    "Treatment Plan",
    "Reports",
    "Alerts"
]

# safe index handling
if st.session_state.page not in pages:
    st.session_state.page = "Dashboard"

menu = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(st.session_state.page),
    key="main_navigation"
)

st.session_state.page = menu


# ------------------- ROUTING -------------------
if menu == "Dashboard":
    dashboard.show()

elif menu == "Patient Details":
    patient_details.show()

elif menu == "Live Monitoring":
    live_monitoring.show()

elif menu == "Trend Analysis":
    trend_analysis.show()

elif menu == "Risk Analysis":
    risk_analysis.show()

elif menu == "Treatment Plan":
    treatment_plan.show()

elif menu == "Reports":
    reports.show()

elif menu == "Alerts":
    alerts.show()


# ------------------ STORE HISTORY (REAL-TIME EFFECT) ------------------
def update_history(key, value):
    # Ensure the key exists before appending
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append(value)
    if len(st.session_state[key]) > 60:
        st.session_state[key].pop(0)