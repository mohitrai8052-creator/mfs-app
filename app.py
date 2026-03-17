import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import random
from datetime import datetime, timedelta
import io

def generate_sbi_perfect_data(opening_bal, salary_text):
    data = []
    curr_bal = opening_bal
    data.append(["Txn Date", "Value\nDate", "Description", "Ref No./Cheque\nNo.", "Debit", "Credit", "Balance"])
    
    start_date = datetime(2025, 10, 6)
    for i in range(150):
        d = start_date - timedelta(hours=i*24/0.95)
        d_str = d.strftime("%d %b %Y")
        if d.day in [5, 6, 7] and i % 25 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        else:
            ref = f"{random.randint(100000000000, 999999999999)}"
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(100, 3500)
        curr_bal = curr_bal + dep - wit
        data.append([d_str, d_str, desc, "", f"{wit:,.2f}" if wit>0 else "", f"{dep:,.2f}" if dep>0 else "", f"{curr_bal:,.2f}"])
    return data

st.set_page_config(layout="wide")
st.title("🏦 SBI Professional Output")

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Acc No", "00000031144336469")
with c2:
    br = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFSC", "SBIN0030082")
    cif = st.text_input("CIF", "85774527603")
    op_bal = st.number_input("Opening Bal", value=42.37)

if st.button("🚀 Process Statement"):
    st.session_state.final_v3 = generate_sbi_perfect_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success("Done!")

if "final_v3" in st.session_state:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, rightMargin=15, leftMargin=15, topMargin=20, bottomMargin=20)
    elements = []
    
    # Header
    elements.append(Paragraph("<b>SBI</b>", ParagraphStyle('H', fontSize=20, fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 10))
    
    # Detail Table (Precise Columns)
    detail_style = ParagraphStyle('D', fontSize=8, leading=10)
    d_rows = [
        [Paragraph(f"Account Name : {name}", detail_style), Paragraph(f"Account Number : {acc}", detail_style)],
        [Paragraph(f"Address : {addr}", detail_style), Paragraph(f"Branch : {br}", detail_style)],
        [Paragraph("Date : 6 Oct 2025", detail_style), Paragraph(f"CIF No : {cif}", detail_style)],
        [Paragraph("Account Description : SBCHQ-RSP-PUBIND", detail_style), Paragraph(f"IFS Code : {ifsc}", detail_style)]
    ]
    dt = Table(d_rows, colWidths=[280, 280])
    dt.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP')]))
    elements.append(dt)
    elements.append(Spacer(1, 15))
    
    elements.append(Paragraph("Account Statement from 7 Apr 2025 to 6 Oct 2025", ParagraphStyle('N', fontSize=8.5)))
    elements.append(Spacer(1, 10))

    # Master Table Layout
    t = Table(st.session_state.final_v3, colWidths=[55, 55, 185, 55, 65, 65, 80], repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('LINEABOVE', (0,0), (-1,0), 0.5, colors.black),
        ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
        ('ALIGN', (4,0), (-1,-1), 'RIGHT'),
        ('ALIGN', (5,0), (-1,-1), 'RIGHT'),
        ('ALIGN', (6,0), (-1,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
    ]))
    elements.append(t)
    doc.build(elements)
    st.download_button("📥 Download Final PDF", buf.getvalue(), "SBI_Statement_Pro.pdf")
