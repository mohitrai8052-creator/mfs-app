import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import random
from datetime import datetime, timedelta
import io

def generate_bank_data(op_bal, sal_text):
    data = []
    curr_bal = op_bal
    # Header Row - Exact SBI Wording
    data.append(["Txn Date", "Value Date", "Description", "Ref No./Cheque No.", "Debit", "Credit", "Balance"])
    start = datetime(2025, 10, 6)
    for i in range(120): # 120 Entries
        d = start - timedelta(hours=i*36)
        d_str = d.strftime("%d %b %Y")
        if d.day in [6, 7] and i % 20 == 0:
            desc, dep, wit = sal_text, 80000.0, 0.0
        else:
            ref = f"{random.randint(100000000000, 999999999999)}"
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(100, 5000)
        curr_bal = curr_bal + dep - wit
        data.append([d_str, d_str, desc, "", f"{wit:,.2f}" if wit>0 else "", f"{dep:,.2f}" if dep>0 else "", f"{curr_bal:,.2f}"])
    return data

st.title("🏦 SBI Final Master Copy")

# Input Section
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Account Number", "00000031144336469")
with c2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFSC", "SBIN0030082")
    cif = st.text_input("CIF", "85774527603")
    op_bal = st.number_input("Opening Bal", value=42.37)

if st.button("🚀 Apply Bank Format"):
    st.session_state.final_v5 = generate_bank_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success("Layout Finalized!")

if "final_v5" in st.session_state:
    if st.button("📥 Download Final Statement"):
        buf = io.BytesIO()
        # Narrow margins for authentic look
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=25, bottomMargin=25)
        elements = []
        
        # Header - Fixed Font Style
        elements.append(Paragraph("<b>SBI</b>", ParagraphStyle('H', fontSize=18, fontName='Courier-Bold')))
        elements.append(Spacer(1, 10))
        
        # Info Table
        info_s = ParagraphStyle('I', fontSize=8, fontName='Courier', leading=10)
        info_data = [
            [Paragraph(f"Account Name : {name}", info_s), Paragraph(f"Account Number : {acc}", info_s)],
            [Paragraph(f"Address : {addr}", info_s), Paragraph(f"Branch : {branch}", info_s)],
            [Paragraph("Date : 6 Oct 2025", info_s), Paragraph(f"CIF No : {cif}", info_s)],
            [Paragraph("Account Description : SBCHQ", info_s), Paragraph(f"IFS Code : {ifsc}", info_s)]
        ]
        it = Table(info_data, colWidths=[270, 270])
        elements.append(it)
        elements.append(Spacer(1, 15))
        
        # Main Table - Using 'Courier' for bank-computer look
        t = Table(st.session_state.final_v5, colWidths=[60, 60, 165, 55, 65, 65, 75], repeatRows=1)
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'Courier'),
            ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('ALIGN', (4,0), (-1,-1), 'RIGHT'),
            ('ALIGN', (5,0), (-1,-1), 'RIGHT'),
            ('ALIGN', (6,0), (-1,-1), 'RIGHT'),
            ('LINEABOVE', (0,0), (-1,0), 0.5, colors.black),
            ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ]))
        elements.append(t)
        doc.build(elements)
        st.download_button("Download Now", buf.getvalue(), "SBI_Final.pdf")
