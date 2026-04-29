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

# Get page from query params first, fallback to session state
params = st.query_params
if "page" in params and params["page"] in pages:
    current_page = params["page"]
elif st.session_state.page in pages:
    current_page = st.session_state.page
else:
    current_page = "Dashboard"

default_index = pages.index(current_page)

# Sidebar radio for user clicks (optional - for UX)
menu = st.sidebar.radio("Navigation", pages, index=default_index, key="main_navigation")

# Update query params when radio is clicked
if menu != current_page:
    st.query_params["page"] = menu

# Use current_page for routing (not menu!)
st.session_state.page = current_page


# ------------------- ROUTING -------------------
if current_page == "Dashboard":
    dashboard.show()

elif current_page == "Patient Details":
    patient_details.show()

elif current_page == "Live Monitoring":
    live_monitoring.show()

elif current_page == "Trend Analysis":
    trend_analysis.show()

elif current_page == "Risk Analysis":
    risk_analysis.show()

elif current_page == "Treatment Plan":
    treatment_plan.show()

elif current_page == "Reports":
    reports.show()

elif current_page == "Alerts":
    alerts.show()


# ------------------ STORE HISTORY (REAL-TIME EFFECT) ------------------
def update_history(key, value):
    # Ensure the key exists before appending
    if key not in st.session_state:
        st.session_state[key] = []
    st.session_state[key].append(value)
    if len(st.session_state[key]) > 60:
        st.session_state[key].pop(0)