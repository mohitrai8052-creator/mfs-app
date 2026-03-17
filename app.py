import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
from datetime import datetime, timedelta
import io

def generate_sbi_data(op_bal, sal_text):
    data = []
    curr_bal = op_bal
    curr_date = datetime(2025, 10, 6, 10, 0)
    end_date = datetime(2025, 4, 7, 9, 0)
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        if curr_date.day in [5, 6, 7] and random.random() > 0.8:
            desc, dep, wit = sal_text, 80000.0, 0.0
        else:
            ref = str(random.randint(100000000000, 999999999999))
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(100, 5000)
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "wit": wit, "dep": dep, "bal": curr_bal})
        curr_date -= timedelta(hours=random.randint(15, 45))
    return data

st.title("🏦 SBI Original Property Final Fix")

# Inputs
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Acc No.", "00000031144336469")
with c2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFSC", "SBIN0030082")
    cif = st.text_input("CIF", "85774527603")
    op_bal = st.number_input("Opening Bal (7 Apr)", value=42.37)

if st.button("🚀 Final Step: Fix Producer Name"):
    st.session_state.master_6m_final = generate_sbi_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success("Data Ready! Click Download to see iText Properties.")

if "master_6m_final" in st.session_state:
    if st.button("📥 Download PDF"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        c.setPDFVersion(1, 4)
        
        # Standard Info
        c.setAuthor("State Bank of India")
        c.setTitle("Statement_Account")

        def draw_template(can):
            can.setFont("Helvetica-Bold", 16)
            can.drawString(20*mm, 282*mm, "SBI")
            can.setFont("Courier", 8.2)
            can.drawString(20*mm, 272*mm, f"Account Name   : {name}")
            can.drawString(115*mm, 272*mm, f"Account Number : {acc}")
            can.drawString(20*mm, 267*mm, f"Address        : {addr.splitlines()[0]}")
            can.drawString(115*mm, 267*mm, f"Branch         : {branch}")
            can.drawString(20*mm, 245*mm, "Date           : 6 Oct 2025")
            can.drawString(115*mm, 255*mm, f"IFS Code       : {ifsc}")
            can.setFont("Courier-Bold", 9)
            can.drawString(20*mm, 232*mm, "Account Statement from 7 Apr 2025 to 6 Oct 2025")
            can.setLineWidth(0.1)
            can.line(18*mm, 227*mm, 195*mm, 227*mm)
            can.setFont("Courier-Bold", 7.5)
            can.drawString(20*mm, 223*mm, "Txn Date")
            can.drawString(42*mm, 223*mm, "Value Date")
            can.drawString(68*mm, 223*mm, "Description")
            can.drawRightString(148*mm, 223*mm, "Debit")
            can.drawRightString(170*mm, 223*mm, "Credit")
            can.drawRightString(192*mm, 223*mm, "Balance")
            can.line(18*mm, 219*mm, 195*mm, 219*mm)
            return 215*mm

        y = draw_template(c)
        c.setFont("Courier", 7)
        for row in st.session_state.master_6m_final:
            c.drawString(20*mm, y, row['d'])
            c.drawString(42*mm, y, row['d'])
            c.drawString(68*mm, y, row['desc'][:58])
            if row['wit'] > 0: c.drawRightString(148*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(170*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 4.2*mm
            if y < 20*mm:
                c.showPage()
                y = draw_template(c)
                c.setFont("Courier", 7)
        
        c.save()
        
        # --- THE MAGIC TRICK ---
        # PDF ke raw data mein ReportLab ko mita kar iText likhna
        pdf_data = buf.getvalue()
        # ReportLab name replace with exact iText string
        final_pdf = pdf_data.replace(b"ReportLab PDF Library", b"iText 2.1.7 by 1T3XT")
        final_pdf = final_pdf.replace(b"ReportLab", b"iText")
        
        st.download_button("📥 Download Official v1.4 PDF", final_pdf, "SBI_Statement.pdf")
