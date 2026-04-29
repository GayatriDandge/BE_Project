import streamlit as st
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
    st.markdown('<div class="title">💊 Treatment & Action Plan</div>', unsafe_allow_html=True)

    # 🔥 MongoDB Data
    db = get_latest_data()
    if isinstance(db, list):
        db = db[0] if len(db) > 0 else {}
    data = {
        "heart_rate": db.get("avgHeartRate", 110),
        "spo2": db.get("avgSpo2", 95),
        "temp": db.get("skinTempC", 37),
        "bp": db.get("bp", 120)
    }

    # ------------------ CURRENT STATUS ------------------
    st.markdown("### 🧠 Current Condition")

    # Dynamic status (based on real data)
    if data["spo2"] < 92 or data["heart_rate"] > 120:
        status = "High Risk"
        desc = "Patient showing critical vitals. Immediate attention required."
    elif data["spo2"] < 95 or data["heart_rate"] > 100:
        status = "Moderate Risk"
        desc = "Patient showing elevated HR and mild hypoxia."
    else:
        status = "Stable"
        desc = "Vitals are within normal range."

    st.markdown(f"""
    <div class="card">
        <p><b>Status:</b> {status}</p>
        <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ TREATMENT SUGGESTIONS ------------------
    st.markdown("### 🩺 Suggested Interventions")

    st.markdown("""
    <div class="card">
    <ul>
        <li>Administer oxygen support (2–4 L/min)</li>
        <li>Monitor heart rate continuously</li>
        <li>Check for infection (fever present)</li>
        <li>Maintain hydration</li>
        <li>Re-evaluate vitals every 10 minutes</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ MEDICATION PLAN ------------------
    st.markdown("### 💉 Medication Plan")

    med1 = st.checkbox("Paracetamol (Fever control)")
    med2 = st.checkbox("Beta Blocker (HR control)")
    med3 = st.checkbox("Oxygen Therapy")

    # ------------------ PRIORITY ACTION ------------------
    st.markdown("### 🚨 Priority Action")

    action = st.selectbox(
        "Select Immediate Action",
        ["Monitor", "Administer Oxygen", "Call Doctor", "Shift to ICU"]
    )

    st.markdown(f"""
    <div class="card">
        <p><b>Selected Action:</b> {action}</p>
    </div>
    """, unsafe_allow_html=True)

    # ------------------ NOTES ------------------
    st.markdown("### 📝 Doctor Instructions")

    notes = st.text_area("Write treatment instructions")

    # ------------------ SAVE BUTTON ------------------
    if st.button("Save Plan"):
        st.success("Treatment plan saved successfully")

    # ------------------ SUMMARY ------------------
    st.markdown("### 📋 Plan Summary")

    st.markdown(f"""
    <div class="card">
        <p><b>Medications:</b> 
        {"Paracetamol " if med1 else ""}
        {"Beta Blocker " if med2 else ""}
        {"Oxygen " if med3 else ""}</p>

        <p><b>Action:</b> {action}</p>
        <p><b>Notes:</b> {notes}</p>
    </div>
    """, unsafe_allow_html=True)