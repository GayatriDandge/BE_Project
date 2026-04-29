from fpdf import FPDF
from datetime import datetime


def generate_report(patient_name, vitals, risk):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Patient Health Report", ln=True, align="C")

    pdf.ln(5)

    # Patient Info
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Patient Name: {patient_name}", ln=True)
    pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(5)

    # Vitals Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Vitals", ln=True)

    pdf.set_font("Arial", size=12)
    for key, value in vitals.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)

    pdf.ln(5)

    # Risk Section
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Risk Assessment", ln=True)

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Risk Level: {risk}", ln=True)

    # Save file
    file_name = f"{patient_name}_report.pdf"
    pdf.output(file_name)

    return file_name