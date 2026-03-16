import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
from datetime import datetime, timedelta
import io

# --- High Precision Data Generator ---
def get_final_data(opening_bal, salary_text):
    data = []
    curr_bal = opening_bal
    # Header Row
    data.append(["Txn Date", "Value Date", "Description", "Ref No./Cheque No.", "Debit", "Credit", "Balance"])
    
    start_date = datetime(2025, 10, 6)
    for i in range(150):
        d = start_date - timedelta(days=i*0.4)
        d_str = d.strftime("%d %b %Y")
        
        if d.day in [6, 7] and i % 25 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        else:
            ref = f"{random.randint(100000000000, 999999999999)}"
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(100, 2500)
        
        curr_bal = curr_bal + dep - wit
        data.append([d_str, d_str, desc, "", f"{wit:,.2f}" if wit>0 else "", f"{dep:,.2f}" if dep>0 else "", f"{curr_bal:,.2f}"])
    return data

st.set_page_config(layout="wide")
st.title("🏦 SBI Professional Layout System")

# Layout Inputs
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Account Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Account Number", "00000031144336469")
with c2:
    br = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFS Code", "SBIN0030082")
    cif = st.text_input("CIF No.", "85774527603")
    op_bal = st.number_input("Opening Balance", value=42.37)

sal_desc = st.text_input("Salary Narration", "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")

if st.button("🚀 Step 1: Fix All Alignments"):
    st.session_state.final_sbi = get_final_data(op_bal, sal_desc)
    st.success("Layout Ready!")

if "final_sbi" in st.session_state:
    if st.button("📥 Step 2: Download Exact PDF"):
        buf = io.BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=25, leftMargin=25, topMargin=30, bottomMargin=30)
        elements = []
        
        # 1. SBI Logo/Header
        elements.append(Paragraph("<b>SBI</b>", ParagraphStyle('SBI', fontSize=18, fontName='Helvetica-Bold')))
        elements.append(Spacer(1, 20))
        
        # 2. Details Block (2 Columns)
        d_data = [
            [f"Account Name : {name}", f"Account Number : {acc}"],
            [f"Address : {addr}", f"Branch : {br}"],
            ["Date : 6 Oct 2025", f"CIF No : {cif}"],
            ["Account Description : SBCHQ-RSP-PUBIND", f"IFS Code : {ifsc}"]
        ]
        dt = Table(d_data, colWidths=[260, 260])
        dt.setStyle(TableStyle([
            ('FONTSIZE', (0,0), (-1,-1), 8.5),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        elements.append(dt)
        elements.append(Spacer(1, 20))
        
        elements.append(Paragraph("Account Statement from 7 Apr 2025 to 6 Oct 2025", ParagraphStyle('N', fontSize=9)))
        elements.append(Spacer(1, 10))

        # 3. Main Transaction Table (Professional Grid)
        t = Table(st.session_state.final_sbi, colWidths=[62, 62, 160, 50, 60, 60, 75], repeatRows=1)
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('ALIGN', (4,0), (-1,-1), 'RIGHT'), # Debit
            ('ALIGN', (5,0), (-1,-1), 'RIGHT'), # Credit
            ('ALIGN', (6,0), (-1,-1), 'RIGHT'), # Balance
            ('LINEABOVE', (0,0), (-1,0), 1, colors.black),
            ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
            ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black), # Last line
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ]))
        elements.append(t)
        
        doc.build(elements)
        st.download_button("Download Now", buf.getvalue(), file_name="SBI_Official_Statement.pdf", mime="application/pdf")
