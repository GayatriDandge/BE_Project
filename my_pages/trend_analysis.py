import streamlit as st
import matplotlib.pyplot as plt
import random
from database import get_latest_data   # ✅ ADDED

# ------------------ UI ------------------
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


def show():
    st.markdown('<div class="title">📊 Trend Analysis</div>', unsafe_allow_html=True)

    # ------------------ TIME RANGE ------------------
    time_range = st.selectbox("Select Time Range", ["Last 10 mins", "Last 1 hour", "Last 6 hours"])

    # 🔥 MongoDB Data
    db = get_latest_data()
    if isinstance(db, list):
        db = db[0] if len(db) > 0 else {}

    base_hr = db.get("avgHeartRate", 100)
    base_spo2 = db.get("avgSpo2", 95)
    base_temp = db.get("skinTempC", 37)
    base_bp = db.get("bp", 130)

    # ------------------ DATA (BASED ON REAL VALUES) ------------------
    x = list(range(20))

    hr = [base_hr + random.randint(-10, 10) for _ in x]
    spo2 = [base_spo2 + random.randint(-3, 2) for _ in x]
    temp = [base_temp + random.uniform(-0.5, 0.5) for _ in x]
    bp = [base_bp + random.randint(-10, 10) for _ in x]

    # ------------------ STATUS DETECTION ------------------
    def trend_status(data):
        if data[-1] > data[0]:
            return "⬆ Worsening"
        return "⬇ Improving"

    # ------------------ CARDS ------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f'<div class="card"><h4>❤️ HR</h4><p>{trend_status(hr)}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><h4>🫁 SpO2</h4><p>{trend_status(spo2)}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><h4>🌡 Temp</h4><p>{trend_status(temp)}</p></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="card"><h4>🩸 BP</h4><p>{trend_status(bp)}</p></div>', unsafe_allow_html=True)

    # ------------------ GRAPHS ------------------
    st.markdown("### 📈 Vital Trends")

    fig1, ax1 = plt.subplots()
    ax1.plot(hr)
    ax1.set_title("Heart Rate Trend")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.plot(spo2)
    ax2.set_title("SpO2 Trend")
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots()
    ax3.plot(temp)
    ax3.set_title("Temperature Trend")
    st.pyplot(fig3)

    fig4, ax4 = plt.subplots()
    ax4.plot(bp)
    ax4.set_title("Blood Pressure Trend")
    st.pyplot(fig4)

    # ------------------ INSIGHT ------------------
    st.markdown("### 🧠 Clinical Insight")

    if hr[-1] > 110:
        st.warning("Heart rate trend indicates stress or tachycardia")

    if spo2[-1] < 92:
        st.error("SpO2 declining — possible respiratory issue")

    if temp[-1] > 38:
        st.warning("Temperature rising — possible infection")

    if bp[-1] > 140:
        st.warning("Blood pressure elevated")