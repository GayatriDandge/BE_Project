import streamlit as st

def show_environment(data):
    st.markdown("### 🌡 Room Environment")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("AQI", data["aqi"])
    col2.metric("CO2 (ppm)", data["co2"])
    col3.metric("Smoke", data["smoke"])
    col4.metric("Ammonia", data["ammonia"])

    st.markdown("---")