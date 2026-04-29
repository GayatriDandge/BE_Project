import streamlit as st
import random

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

.badge {
    padding: 6px 12px;
    border-radius: 20px;
    color: white;
    font-size: 14px;
}

.green { background-color: #2ecc71; }
.yellow { background-color: #f1c40f; }
.red { background-color: #e74c3c; }

</style>
""", unsafe_allow_html=True)


# ------------------ RISK MODEL ------------------
def calculate_risk(data):
    score = 0

    if data["heart_rate"] > 120:
        score += 30
    elif data["heart_rate"] > 100:
        score += 15

    if data["spo2"] < 92:
        score += 30
    elif data["spo2"] < 95:
        score += 15

    if data["temp"] > 38:
        score += 20

    if data["bp"] > 140:
        score += 20

    return min(score, 100)


def risk_label(score):
    if score < 30:
        return "LOW", "green"
    elif score < 70:
        return "MEDIUM", "yellow"
    return "HIGH", "red"


# ------------------ MAIN ------------------
def show():
    st.markdown('<div class="title">🧠 AI Risk Analysis</div>', unsafe_allow_html=True)

    # ------------------ DATA ------------------
    data = {
        "temp": 38.2,
        "heart_rate": 118,
        "spo2": 93,
        "bp": 145
    }

    # ------------------ RISK SCORE ------------------
    score = calculate_risk(data)
    label, color = risk_label(score)

    st.markdown("### 📊 Risk Score")

    st.markdown(f"""
    <div class="card">
        <h2>Risk Level: <span class="badge {color}">{label}</span></h2>
        <h3>Score: {score}/100</h3>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ PROGRESS BAR ------------------
    st.markdown("### 📈 Risk Meter")
    st.progress(score / 100)

    # ------------------ CONTRIBUTION ------------------
    st.markdown("### 🔍 Risk Breakdown")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="card">
            <h4>❤️ Heart Rate</h4>
            <p>{data["heart_rate"]} bpm</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h4>🌡 Temperature</h4>
            <p>{data["temp"]} °C</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <h4>🫁 SpO2</h4>
            <p>{data["spo2"]}%</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <h4>🩸 Blood Pressure</h4>
            <p>{data["bp"]} mmHg</p>
        </div>
        """, unsafe_allow_html=True)

    # ------------------ ALERTS ------------------
    st.markdown("### 🚨 Risk Alerts")

    if data["spo2"] < 92:
        st.error("Critical: Oxygen level dangerously low")

    if data["heart_rate"] > 120:
        st.warning("Warning: Elevated heart rate")

    if data["temp"] > 38:
        st.warning("Fever detected")

    if data["bp"] > 140:
        st.warning("High blood pressure")

    # ------------------ RECOMMENDATIONS ------------------
    st.markdown("### 📝 Recommendations")

    st.markdown("""
    <div class="card">
    <ul>
        <li>Monitor vitals continuously</li>
        <li>Provide oxygen support if SpO2 drops further</li>
        <li>Administer antipyretics for fever</li>
        <li>Consult physician for BP control</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ TREND SIMULATION ------------------
    st.markdown("### 📉 Risk Trend (Simulated)")

    trend = [score + random.randint(-10, 10) for _ in range(10)]
    st.line_chart(trend)