import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh
from database import get_latest_data

# ------------------ AUTO REFRESH ------------------
st_autorefresh(interval=800, key="live_refresh")

# ------------------ SESSION STATE FOR LIVE TREND ------------------
if "hr_history" not in st.session_state:
    st.session_state.hr_history = []
    st.session_state.temp_history = []
    st.session_state.spo2_history = []
    st.session_state.bp_history = []
    st.session_state.ecg_history = []

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
</style>
""", unsafe_allow_html=True)


# ------------------ GRAPH ------------------
def plot_colored_line(title, values, ranges):
    x = np.arange(len(values))

    fig, ax = plt.subplots(figsize=(12, 3))

    for i in range(len(x) - 1):
        val = values[i]

        if ranges["high"][0] <= val <= ranges["high"][1]:
            color = "red"
        elif ranges["medium"][0] <= val <= ranges["medium"][1]:
            color = "orange"
        else:
            color = "green"

        ax.plot(x[i:i+2], values[i:i+2], color=color, linewidth=2)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)

    return fig


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


# ------------------ MAIN ------------------
def show():
    st.markdown('<div class="title">📟 Live ICU Monitoring</div>', unsafe_allow_html=True)

    # 🔥 MongoDB Data
    db = get_latest_data()
    if isinstance(db, list):
        db = db[0] if len(db) > 0 else {}

    data = {
        "temp": db.get("skinTempC", 0),
        "heart_rate": db.get("avgHeartRate", 0),
        "spo2": db.get("avgSpo2", 0),
        "bp": db.get("bp", 124),
        "ecg": db.get("ecgRaw", 3058),
        "aqi": db.get("aqi", 100),
        "co2": db.get("co2", 400),
        "smoke": db.get("smoke", "LOW"),
        "ammonia": db.get("ammonia", "POSSIBLE")
    }

    # ------------------ STORE HISTORY (REAL-TIME EFFECT) ------------------
    def update_history(key, value):
        st.session_state[key].append(value)
        if len(st.session_state[key]) > 60:
            st.session_state[key].pop(0)

    update_history("hr_history", data["heart_rate"])
    update_history("temp_history", data["temp"])
    update_history("spo2_history", data["spo2"])
    update_history("bp_history", data["bp"])
    update_history("ecg_history", data["ecg"])

    # ------------------ ENVIRONMENT ------------------
    show_environment(data)

    # ------------------ TOP CARDS ------------------
    st.markdown("### 🚨 Critical Vitals")

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f'<div class="card"><h4>❤️ HR</h4><h2>{data["heart_rate"]}</h2></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h4>🫁 SpO2</h4><h2>{data["spo2"]}</h2></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><h4>🌡 Temp</h4><h2>{data["temp"]}</h2></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="card"><h4>🩸 BP</h4><h2>{data["bp"]}</h2></div>', unsafe_allow_html=True)

    st.markdown("🟢 Normal  🟡 Warning  🔴 Critical")
    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ GRAPHS ------------------
    st.markdown("### 📊 Live Graphs")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(plot_colored_line("❤️ Heart Rate", st.session_state.hr_history,
        {"low": (60,100), "medium": (100,120), "high": (120,200)}))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(plot_colored_line("🌡 Temperature", st.session_state.temp_history,
        {"low": (36,37.5), "medium": (37.5,38), "high": (38,42)}))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(plot_colored_line("🫁 SpO2", st.session_state.spo2_history,
        {"low": (95,100), "medium": (90,95), "high": (0,90)}))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(plot_colored_line("🩸 Blood Pressure", st.session_state.bp_history,
        {"low": (90,120), "medium": (120,140), "high": (140,200)}))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.pyplot(plot_colored_line("📉 ECG Signal", st.session_state.ecg_history,
        {"low": (2500,3500), "medium": (2000,2500), "high": (0,2000)}))
    st.markdown('</div>', unsafe_allow_html=True)

    # ------------------ ALERTS ------------------
    st.markdown("### 🚨 Alerts")

    if data["spo2"] < 92:
        st.error("Low Oxygen Level!")

    if data["heart_rate"] > 120:
        st.warning("High Heart Rate!")

    if data["temp"] > 38:
        st.error("Fever Detected!")