import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import random
from datetime import datetime, timedelta
import io

# --- Professional Data Generator ---
def generate_sbi_data(opening_bal, salary_text):
    data = []
    curr_bal = opening_bal
    data.append(["Txn Date", "Value Date", "Description", "Ref No.", "Debit", "Credit", "Balance"])
    
    # 6 mahine ka data (April se October)
    start_date = datetime(2025, 10, 6)
    for i in range(150):
        d = start_date - timedelta(hours=i*24/1.2)
        d_str = d.strftime("%d %b %Y")
        
        # Salary Logic (Har mahine ki 6 ya 7 tareekh)
        if d.day in [6, 7] and i % 25 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        else:
            ref = random.randint(100000000000, 999999999999)
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(50, 3000)
        
        curr_bal = curr_bal + dep - wit
        data.append([d_str, d_str, desc, "", f"{wit:,.2f}" if wit>0 else "", f"{dep:,.2f}" if dep>0 else f"{curr_bal:,.2f}"])
    return data

st.set_page_config(page_title="SBI Official Copy", layout="wide")
st.title("🏦 SBI Professional Statement System")

# User Inputs (Aapki file ke hisab se default values)
col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Account Name", "Mr. ASHISH TIWARI")
    address = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc_no = st.text_input("Account Number", "00000031144336469")
with col2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFS Code", "SBIN0030082")
    cif = st.text_input("CIF No.", "85774527603")
    opening_bal = st.number_input("Opening Balance (7 Apr 2025)", value=42.37)

salary_val = st.text_input("Salary Narration", "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")

if st.button("🚀 Step 1: Generate 150 Entries"):
    st.session_state.sbi_final = generate_sbi_data(opening_bal, salary_val)
    st.success("Data Taiyar Hai!")

if "sbi_final" in st.session_state:
    if st.button("📥 Step 2: Download Professional PDF"):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
        elements = []
        styles = getSampleStyleSheet()
        
        # Header
        elements.append(Paragraph("<b>SBI</b>", ParagraphStyle('SBI', fontSize=16, fontName='Helvetica-Bold')))
        elements.append(Spacer(1, 10))
        
        # Details Table (Left & Right Column)
        header_data = [
            [f"Account Name: {name}", f"Account Number: {acc_no}"],
            [f"Address: {address}", f"Branch: {branch}"],
            [f"Date: 6 Oct 2025", f"CIF No: {cif}"],
            ["", f"IFS Code: {ifsc}"]
        ]
        ht = Table(header_data, colWidths=[250, 250])
        ht.setStyle(TableStyle([('FONTSIZE', (0,0), (-1,-1), 9), ('VALIGN', (0,0), (-1,-1), 'TOP')]))
        elements.append(ht)
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("Account Statement from 7 Apr 2025 to 6 Oct 2025", styles['Normal']))
        elements.append(Spacer(1, 10))

        # Main Table
        t = Table(st.session_state.sbi_final, colWidths=[60, 60, 180, 40, 60, 60, 70])
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
        st.download_button("Download Now", buf.getvalue(), file_name="SBI_Statement_Pro.pdf", mime="application/pdf")
