import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import random
from datetime import datetime, timedelta
import io

# --- Professional Data Generator ---
def get_sbi_data(opening_bal, salary_text):
    data = []
    curr_bal = opening_bal
    data.append(["Txn Date", "Value Date", "Description", "Ref No.", "Debit", "Credit", "Balance"])
    start_date = datetime(2025, 10, 6)
    for i in range(40):
        d = start_date - timedelta(days=i)
        d_str = d.strftime("%d %b %Y")
        if i % 15 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        else:
            desc, dep, wit = f"TRANSFER-UPI/DR/{random.randint(100000,999999)}/PAYTM", 0.0, random.uniform(100, 2000)
        curr_bal = curr_bal + dep - wit
        data.append([d_str, d_str, desc, "", f"{wit:,.2f}" if wit>0 else "", f"{dep:,.2f}" if dep>0 else "", f"{curr_bal:,.2f}"])
    return data

st.set_page_config(page_title="SBI Official Copy", layout="wide")
st.title("🏦 SBI Professional Statement System")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Account Name", "MOHIT KUMAR RAI")
    acc_no = st.text_input("Account Number", "00000031144336469")
with col2:
    opening_bal = st.number_input("Opening Balance", value=42.37)
    salary_val = st.text_input("Salary Narration", "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")

if st.button("🚀 Step 1: Generate Data"):
    st.session_state.sbi_final = get_sbi_data(opening_bal, salary_val)
    st.success("Data Taiyar Hai!")

if "sbi_final" in st.session_state:
    if st.button("📥 Step 2: Download Official PDF"):
        buf = io.BytesIO()
        # ReportLab engine (iText compatible)
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
        doc.title = "Account Statement"
        
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph("<b>SBI</b>", ParagraphStyle('SBI', fontSize=14, fontName='Helvetica-Bold')))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(f"Account Name : {name}", ParagraphStyle('L', fontSize=9)))
        elements.append(Paragraph(f"Account Number : {acc_no}", ParagraphStyle('L', fontSize=9)))
        elements.append(Spacer(1, 15))

        # Table formatting for perfect alignment
        t = Table(st.session_state.sbi_final, colWidths=[65, 65, 170, 45, 60, 60, 70])
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('ALIGN', (4,0), (-1,-1), 'RIGHT'),
            ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(t)
        
        doc.build(elements)
        st.download_button("Download Now", buf.getvalue(), file_name="SBI_Statement.pdf", mime="application/pdf")
