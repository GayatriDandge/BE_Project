import streamlit as st
from streamlit_autorefresh import st_autorefresh   # ✅ added
from database import get_latest_data   
from database import collection                  # ✅ MongoDB

# 🔴 AUTO REFRESH
st_autorefresh(interval=3000, key="home_refresh")

def show():

    # ------------------ TITLE ------------------
    st.markdown("<div class='title'>🏥 HealthSync AI Dashboard</div>", unsafe_allow_html=True)

    # ------------------ TOP STATS (MODERN CARDS) ------------------
    st.markdown("### Hospital Overview")

    st.markdown("""
    <style>
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        text-align: center;
    }

    .patient-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        transition: 0.3s;
    }

    .patient-card:hover {
        transform: translateY(-3px);
    }

    .blur-card {
        background: white;
        padding: 15px;
        border-radius: 15px;
        filter: blur(5px);
        opacity: 0.5;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
    }

    .badge-high {
        color: white;
        background: red;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 12px;
    }

    .badge-med {
        color: white;
        background: orange;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 12px;
    }

    .badge-low {
        color: white;
        background: green;
        padding: 4px 10px;
        border-radius: 10px;
        font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    # 🔥 Fetch data from DB
    db_data = list(collection.find().limit(50))

    total = len(db_data)
    critical = 0
    medium = 0
    stable = 0

    patients = []

    for d in db_data:
        hr = d.get("avgHeartRate", 0)
        spo2 = d.get("avgSpo2", 100)

        if spo2 < 92:
            priority = "HIGH"
            critical += 1
        elif hr > 110:
            priority = "MEDIUM"
            medium += 1
        else:
            priority = "LOW"
            stable += 1

        patients.append({
            "name": f"Patient {str(d['_id'])[-4:]}",
            "priority": priority
        })

    # ------------------ STATS ------------------
    col1.markdown(f"<div class='stat-card'><h4>Total Patients</h4><h2>{total}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='stat-card'><h4>Critical</h4><h2 style='color:red'>{critical}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='stat-card'><h4>Medium</h4><h2 style='color:orange'>{medium}</h2></div>", unsafe_allow_html=True)
    col4.markdown(f"<div class='stat-card'><h4>Stable</h4><h2 style='color:green'>{stable}</h2></div>", unsafe_allow_html=True)

    # ------------------ PATIENTS ------------------
    st.markdown("## 🧑‍⚕️ Patient Severity Index")

    # ------------------ FIRST ROW HEADER ------------------
    col1, col2, col3 = st.columns([1, 4, 2])
    col1.markdown("**#**")
    col2.markdown("**Patient Card**")
    col3.markdown("**Action**")

    # ------------------ PATIENT LIST ------------------
    for i, p in enumerate(patients[:4]):   # limit to 4 like your UI

        col1, col2, col3 = st.columns([1, 4, 2])

        if p["priority"] == "HIGH":
            badge = "<span class='badge-high'>HIGH</span>"
        elif p["priority"] == "MEDIUM":
            badge = "<span class='badge-med'>MEDIUM</span>"
        else:
            badge = "<span class='badge-low'>LOW</span>"

        # FIRST PATIENT
        if i == 0:

            col1.markdown(f"<div style='font-size:18px;font-weight:bold'>{i+1}</div>", unsafe_allow_html=True)

            col2.markdown(f"""
            <div class='patient-card'>
                <h3>👤 {p['name']}</h3>
                <p>{badge}</p>
                <p>Status: ACTIVE MONITORING</p>
            </div>
            """, unsafe_allow_html=True)

            if col3.button("View Details", key=f"btn_{i}"):
                st.session_state["selected_patient"] = p["name"]
                st.session_state["page"] = "Patient Details"
                st.session_state["main_navigation"] = "Patient Details"  # Add this line
                st.rerun()

        # OTHER PATIENTS
        else:

            col1.markdown(f"<div style='font-size:18px;font-weight:bold'>{i+1}</div>", unsafe_allow_html=True)

            col2.markdown(f"""
            <div class='blur-card'>
                <h3>👤 {p['name']}</h3>
                <p>{badge}</p>
                <p>🔒 Locked Patient Data</p>
            </div>
            """, unsafe_allow_html=True)

            col3.markdown("<div style='opacity:0.4'>🔒 Restricted</div>", unsafe_allow_html=True)