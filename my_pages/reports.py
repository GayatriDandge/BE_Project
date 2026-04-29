import streamlit as st
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import matplotlib.pyplot as plt
import random
import os
from streamlit_autorefresh import st_autorefresh     # ✅ added
from database import get_latest_data                 # ✅ added

# 🔴 AUTO REFRESH
st_autorefresh(interval=4000, key="report_refresh")

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

# ------------------ RISK ------------------
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
        return "MODERATE", "yellow"
    return "HIGH", "red"

# ------------------ CHART ------------------
def create_chart(data):
    x = list(range(10))
    hr = [data["heart_rate"] + random.randint(-5, 5) for _ in x]
    spo2 = [data["spo2"] + random.randint(-2, 2) for _ in x]
    temp = [data["temp"] + random.uniform(-0.5, 0.5) for _ in x]

    plt.figure(figsize=(6, 3))
    plt.plot(x, hr, label="Heart Rate")
    plt.plot(x, spo2, label="SpO2")
    plt.plot(x, temp, label="Temp")
    plt.legend()
    plt.title("Vitals Trend")

    chart_path = "vitals_chart.png"
    plt.savefig(chart_path)
    plt.close()

    return chart_path

# ------------------ PDF ------------------
def generate_pdf(data, score, label, notes):
    file_path = "patient_report.pdf"
    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("PATIENT CLINICAL REPORT", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Name: {data['name']}", styles["Normal"]))
    content.append(Paragraph(f"Age: {data['age']}", styles["Normal"]))
    content.append(Paragraph(f"Gender: {data['gender']}", styles["Normal"]))
    content.append(Paragraph(f"Date: {datetime.now()}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Vitals:", styles["Heading2"]))
    content.append(Paragraph(f"Heart Rate: {data['heart_rate']}", styles["Normal"]))
    content.append(Paragraph(f"SpO2: {data['spo2']}", styles["Normal"]))
    content.append(Paragraph(f"Temperature: {data['temp']}", styles["Normal"]))
    content.append(Paragraph(f"Blood Pressure: {data['bp']}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Risk Assessment:", styles["Heading2"]))
    content.append(Paragraph(f"Risk Level: {label}", styles["Normal"]))
    content.append(Paragraph(f"Score: {score}/100", styles["Normal"]))

    content.append(Spacer(1, 10))

    chart_path = create_chart(data)
    content.append(Paragraph("Vitals Trend Chart:", styles["Heading2"]))
    content.append(Image(chart_path, width=400, height=200))

    content.append(Spacer(1, 10))

    content.append(Paragraph("Doctor Notes:", styles["Heading2"]))
    content.append(Paragraph(notes if notes else "No notes provided", styles["Normal"]))

    doc.build(content)

    if os.path.exists(chart_path):
        os.remove(chart_path)

    return file_path

# ------------------ MAIN ------------------
def show():
    st.markdown('<div class="title">📄 Patient Clinical Report</div>', unsafe_allow_html=True)

    # 🔥 FETCH FROM MONGODB
    db = get_latest_data()
    if isinstance(db, list):
        db = db[0] if len(db) > 0 else {}

    data = {
        "name": f"Patient {str(db.get('_id'))[-4:]}",
        "age": db.get("age", 45),
        "gender": db.get("gender", "Male"),
        "temp": db.get("skinTempC", 0),
        "heart_rate": db.get("avgHeartRate", 0),
        "spo2": db.get("avgSpo2", 0),
        "bp": db.get("bp", 120)
    }

    score = calculate_risk(data)
    label, color = risk_label(score)

    # UI (UNCHANGED)
    st.markdown("### 🧑‍⚕️ Patient Info")
    st.markdown(f"""
    <div class="card">
    <p><b>Name:</b> {data["name"]}</p>
    <p><b>Age:</b> {data["age"]}</p>
    <p><b>Gender:</b> {data["gender"]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧠 Risk")
    st.markdown(f"""
    <div class="card">
    <h3>Risk: <span class="badge {color}">{label}</span></h3>
    <p>Score: {score}/100</p>
    </div>
    """, unsafe_allow_html=True)

    notes = st.text_area("Doctor Notes")

    if st.button("Generate PDF"):
        pdf = generate_pdf(data, score, label, notes)
        with open(pdf, "rb") as f:
            st.download_button("Download Report", f, "patient_report.pdf")