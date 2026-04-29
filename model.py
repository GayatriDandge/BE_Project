def analyze_risk(vitals):
    """
    Analyze patient risk based on vitals
    vitals = {
        "heart_rate": int,
        "spo2": int,
        "bp_sys": int,
        "bp_dia": int,
        "temp": float
    }
    """

    score = 0

    # Heart Rate
    if vitals["heart_rate"] > 120 or vitals["heart_rate"] < 50:
        score += 2

    # Oxygen Level
    if vitals["spo2"] < 90:
        score += 3
    elif vitals["spo2"] < 95:
        score += 1

    # Blood Pressure
    if vitals["bp_sys"] > 160 or vitals["bp_dia"] > 100:
        score += 2

    # Temperature
    if vitals["temp"] > 101:
        score += 2
    elif vitals["temp"] > 99:
        score += 1

    # Final Decision
    if score >= 6:
        return "HIGH RISK"
    elif score >= 3:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"