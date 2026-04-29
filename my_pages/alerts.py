import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh
from database import get_latest_data   # ✅ MongoDB

# 🔴 AUTO REFRESH (real-time feel)
st_autorefresh(interval=2000, key="dashboard_refresh")

# ------------------ CSS ------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #dff5ea, #c7e9d7);
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.title {
    font-size: 28px;
    font-weight: bold;
    color: #065f46;
}

.alert-red {
    background-color: #ffe5e5;
    padding: 15px;
    border-radius: 10px;
    color: #c0392b;
}

.alert-yellow {
    background-color: #fff4cc;
    padding: 15px;
    border-radius: 10px;
    color: #b7950b;
}

.alert-green {
    background-color: #e8f8f5;
    padding: 15px;
    border-radius: 10px;
    color: #1e8449;
}
</style>
""", unsafe_allow_html=True)


# ------------------ ALERT LOGIC ------------------
def get_alerts(data):
    alerts = []

    if data["spo2"] < 92:
        alerts.append(("CRITICAL", "Low Oxygen Level", "red"))

    if data["heart_rate"] > 120:
        alerts.append(("WARNING", "High Heart Rate", "yellow"))

    if data["temp"] > 38:
        alerts.append(("WARNING", "Fever Detected", "yellow"))

    if data["bp"] > 140:
        alerts.append(("WARNING", "High Blood Pressure", "yellow"))

    if not alerts:
        alerts.append(("STABLE", "All vitals normal", "green"))

    return alerts


# ------------------ MAIN ------------------
def show():
    st.markdown('<div class="title">🚨 Patient Alerts Dashboard</div>', unsafe_allow_html=True)

    # 🔥 FETCH FROM MONGODB
    db = get_latest_data()
    if isinstance(db, list):
        db = db[0] if len(db) > 0 else {}

    # ✅ REPLACE DUMMY DATA WITH DB DATA
    data = {
        "heart_rate": db.get("avgHeartRate", 0),
        "spo2": db.get("avgSpo2", 0),
        "temp": db.get("skinTempC", 0),
        "bp": db.get("bp", 120)
    }

    alerts = get_alerts(data)

    # ------------------ CURRENT VITALS ------------------
    st.markdown("### ⚡ Current Vitals")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f'<div class="card"><h4>❤️ HR</h4><h2>{data["heart_rate"]}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h4>🫁 SpO2</h4><h2>{data["spo2"]}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><h4>🌡 Temp</h4><h2>{data["temp"]}</h2></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="card"><h4>🩸 BP</h4><h2>{data["bp"]}</h2></div>', unsafe_allow_html=True)

    # ------------------ ACTIVE ALERTS ------------------
    st.markdown("### 🚨 Active Alerts")

    for level, message, color in alerts:
        if color == "red":
            st.markdown(f'<div class="alert-red"><b>{level}:</b> {message}</div>', unsafe_allow_html=True)
        elif color == "yellow":
            st.markdown(f'<div class="alert-yellow"><b>{level}:</b> {message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alert-green"><b>{level}:</b> {message}</div>', unsafe_allow_html=True)

    # ------------------ PRIORITY PANEL ------------------
    st.markdown("### 🔥 Alert Priority")

    if any(a[0] == "CRITICAL" for a in alerts):
        st.error("Immediate medical attention required")
    elif any(a[0] == "WARNING" for a in alerts):
        st.warning("Patient needs close monitoring")
    else:
        st.success("Patient is stable")

    # ------------------ ALERT HISTORY ------------------
    st.markdown("### 📜 Alert History")

    history = [
        ("10:30", "High BP"),
        ("10:15", "Low SpO2"),
        ("09:50", "Normal"),
    ]

    for time, event in history:
        st.markdown(f"""
        <div class="card">
            <b>{time}</b> — {event}
        </div>
        """, unsafe_allow_html=True)

    # ------------------ ACTIONS ------------------
    st.markdown("### 🩺 Recommended Actions")

    st.markdown("""
    <div class="card">
    <ul>
        <li>Administer oxygen if SpO2 remains low</li>
        <li>Monitor heart rate continuously</li>
        <li>Check for infection (fever)</li>
        <li>Control blood pressure as per protocol</li>
        <li>Escalate to ICU if condition worsens</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ TIMESTAMP ------------------
    st.markdown(f"🕒 Last Updated: {datetime.now().strftime('%H:%M:%S')}")