import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import random
from datetime import datetime, timedelta
import io

# --- High-Fidelity Data Generator ---
def generate_sbi_pro_data(opening_bal, salary_text):
    data = []
    curr_bal = opening_bal
    # Header Row exactly as SBI
    data.append(["Txn Date", "Value\nDate", "Description", "Ref No./Cheque\nNo.", "Debit", "Credit", "Balance"])
    
    start_date = datetime(2025, 10, 6)
    # 150 entries for 6 months
    for i in range(150):
        d = start_date - timedelta(hours=i*24/0.9)
        d_str = d.strftime("%d %b %Y")
        
        if d.day in [5, 6, 7] and i % 25 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        else:
            ref = f"{random.randint(100000000000, 999999999999)}"
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(50, 4000)
        
        curr_bal = curr_bal + dep - wit
        data.append([d_str, d_str, desc, "", f"{wit:,.2f}" if wit>0 else "", f"{dep:,.2f}" if dep>0 else "", f"{curr_bal:,.2f}"])
    return data

st.set_page_config(layout="wide", page_title="SBI Professional")

# --- Inputs ---
st.title("🏦 SBI Final Statement Generator")
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

sal_desc = st.text_input("Salary Description", "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")

if st.button("🔄 Step 1: Process 150 Entries"):
    st.session_state.final_data = generate_sbi_pro_data(op_bal, sal_desc)
    st.success("Data Processing Complete!")

if "final_data" in st.session_state:
    if st.button("📥 Step 2: Download SBI Format PDF"):
        buf = io.BytesIO()
        # Tight margins as per SBI original
        doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=25, bottomMargin=25)
        elements = []
        
        # Heading
        elements.append(Paragraph("<b>SBI</b>", ParagraphStyle('H', fontSize=18, fontName='Helvetica-Bold')))
        elements.append(Spacer(1, 15))
        
        # Info Block
        info_style = ParagraphStyle('I', fontSize=8.5, leading=11)
        d_data = [
            [Paragraph(f"Account Name : {name}", info_style), Paragraph(f"Account Number : {acc}", info_style)],
            [Paragraph(f"Address : {addr}", info_style), Paragraph(f"Branch : {br}", info_style)],
            [Paragraph("Date : 6 Oct 2025", info_style), Paragraph(f"CIF No : {cif}", info_style)],
            [Paragraph("Account Description : SBCHQ-RSP-PUBIND", info_style), Paragraph(f"IFS Code : {ifsc}", info_style)]
        ]
        it = Table(d_data, colWidths=[270, 270])
        it.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
        elements.append(it)
        elements.append(Spacer(1, 15))
        
        elements.append(Paragraph("Account Statement from 7 Apr 2025 to 6 Oct 2025", ParagraphStyle('N', fontSize=9)))
        elements.append(Spacer(1, 10))

        # The Main Table - Exact Column Widths
        t = Table(st.session_state.final_data, colWidths=[58, 58, 175, 55, 65, 65, 75], repeatRows=1)
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 7),
            ('GRID', (0,0), (-1,-1), 0.2, colors.white), # Invisible grid for spacing
            ('LINEABOVE', (0,0), (-1,0), 0.8, colors.black),
            ('LINEBELOW', (0,0), (-1,0), 0.8, colors.black),
            ('ALIGN', (4,0), (-1,-1), 'RIGHT'),
            ('ALIGN', (5,0), (-1,-1), 'RIGHT'),
            ('ALIGN', (6,0), (-1,-1), 'RIGHT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        elements.append(t)
        
        doc.build(elements)
        st.download_button("Click to Download", buf.getvalue(), "SBI_Statement_Final.pdf", "application/pdf")
