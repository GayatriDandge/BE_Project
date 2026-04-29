import streamlit as st
import os
from streamlit_autorefresh import st_autorefresh   # ✅ added
from database import get_latest_data               # ✅ added

# 🔴 AUTO REFRESH
st_autorefresh(interval=3000, key="patient_overview_refresh")

# ------------------ CSS ------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(135deg, #dff5ea, #c7e9d7);
}

/* Card */
.card {
    background: white;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    text-align: center;
}

/* Profile card */
.profile-card {
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

/* Titles */
.title {
    font-size: 28px;
    font-weight: bold;
    color: #065f46;
}

</style>
""", unsafe_allow_html=True)


# ------------------ ENVIRONMENT ------------------
def show_environment(data):
    st.markdown("### 🌡 Room Environment")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="card"><h4>AQI</h4><h2>{data["aqi"]}</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="card"><h4>CO2</h4><h2>{data["co2"]}</h2></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="card"><h4>Smoke</h4><h2>{data["smoke"]}</h2></div>', unsafe_allow_html=True)

    with col4:
        st.markdown(f'<div class="card"><h4>Ammonia</h4><h2>{data["ammonia"]}</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


# ------------------ MAIN ------------------
def show():
    st.markdown('<div class="title">🧑‍⚕️ Patient Overview</div>', unsafe_allow_html=True)

    # 🔥 FETCH FROM MONGODB
    db = get_latest_data()
    if isinstance(db, list):
        db = db[0] if len(db) > 0 else {}   
    data = {
        "name": f"Patient {str(db.get('_id'))[-4:]}",   # dynamic name
        "age": db.get("age", 45),
        "gender": db.get("gender", "Male"),
        "condition": "Under Observation",

        "temp": db.get("skinTempC", 0),
        "heart_rate": db.get("avgHeartRate", 0),
        "spo2": db.get("avgSpo2", 0),
        "bp": db.get("bp", 124),

        "aqi": db.get("aqi", 100),
        "co2": db.get("co2", 400),
        "smoke": db.get("smoke", "LOW"),
        "ammonia": db.get("ammonia", "POSSIBLE")
    }

    # ------------------ ENVIRONMENT ------------------
    show_environment(data)

    # ------------------ PROFILE ------------------
    st.markdown("### 👤 Patient Profile")

    col1, col2 = st.columns([1, 2])

    with col1:
        image_path = os.path.join("assets", "patient.png")
        if os.path.exists(image_path):
            st.image(image_path, width=180)
        else:
            st.warning("Add patient.png in assets folder")

    with col2:
        st.markdown(f"""
        <div class="profile-card">
            <h2>{data["name"]}</h2>
            <p><b>Age:</b> {data["age"]}</p>
            <p><b>Gender:</b> {data["gender"]}</p>
            <p><b>Condition:</b> 
                <span style="background:#f1c40f;padding:6px 12px;border-radius:10px;">
                {data["condition"]}
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ VITALS ------------------
    st.markdown("### ⚡ Current Vitals")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'<div class="card"><h4>❤️ Heart Rate</h4><h2>{data["heart_rate"]}</h2></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="card"><h4>🫁 SpO2</h4><h2>{data["spo2"]}</h2></div>', unsafe_allow_html=True)

    with col3:
        st.markdown(f'<div class="card"><h4>🌡 Temperature</h4><h2>{data["temp"]}</h2></div>', unsafe_allow_html=True)

    with col4:
        st.markdown(f'<div class="card"><h4>🩸 BP</h4><h2>{data["bp"]}</h2></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ DEVICE INFO ------------------
    st.markdown("### 📡 Device Status")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown('<div class="card"><h4>Device</h4><p>Connected</p></div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card"><h4>Signal Quality</h4><p>Good</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ NOTES ------------------
    st.markdown("### 📝 Doctor Notes")
    st.text_area("Write notes here...", height=120)