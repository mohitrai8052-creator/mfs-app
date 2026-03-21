import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
from datetime import datetime, timedelta
import io

# --- 1. Authentic Kotak Data Generator (6 Months) ---
def get_kotak_6m_data(opening_bal):
    transactions = []
    current_bal = opening_bal
    curr_date = datetime(2025, 10, 6)
    end_date = datetime(2025, 4, 7)
    
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        ref_no = f"UPI-{random.randint(600000000000, 699999999999)}"
        
        if curr_date.day in [5, 6, 7] and random.random() > 0.8:
            desc = "CMS-SALARY/TATA MOTORS LTD/OCT25"
            dep, wit = 80000.0, 0.0
        else:
            desc = f"UPI/PAYMENT TO MERCHANT/{random.randint(1000, 9999)}/Payment"
            dep, wit = 0.0, random.uniform(50, 3000)
            
        current_bal = current_bal + dep - wit
        transactions.append({"d": d_str, "desc": desc, "ref": ref_no, "wit": wit, "dep": dep, "bal": current_bal})
        curr_date -= timedelta(hours=random.randint(20, 50))
    return transactions[::-1] # Chronological order

st.title("🏦 Kotak Mahindra Bank - Original Replica")

# Inputs
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Name", "Girase Vinod Rajusing")
    addr = st.text_area("Address", "128 Ratna Prabha Society, Near Bhole Baba Mandir\nParvat Gam, Surat-395010")
    acc_no = st.text_input("Account No.", "9748659761")
with c2:
    crn = st.text_input("CRN", "123456789")
    ifsc = st.text_input("IFSC", "KKBK0000883")
    op_bal = st.number_input("Opening Balance (7 Apr)", value=201.87)

if st.button("🚀 Step 1: Prepare 6-Month Kotak Data"):
    st.session_state.kotak_6m = get_kotak_6m_data(op_bal)
    st.success("Data Generated with Kotak Narrations!")

if "kotak_6m" in st.session_state:
    if st.button("📥 Step 2: Download v1.5 OpenPDF Statement"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        
        # --- TECHNICAL METADATA AS PER YOUR FILE ---
        c.setPDFVersion(1, 5)
        c._doc.info.producer = "OpenPDF 2.0.3"
        c._doc.info.creator = "OpenPDF 2.0.3"
        c.setAuthor("Kotak Mahindra Bank")
        c.setTitle("Account Statement")

        def draw_kotak_template(can, p_num):
            can.setFont("Helvetica-Bold", 14)
            can.drawString(20*mm, 280*mm, "kotak")
            can.setFont("Helvetica", 8)
            can.drawString(20*mm, 270*mm, f"Account No: {acc_no}")
            can.drawString(20*mm, 265*mm, f"CRN: {crn}")
            can.drawString(150*mm, 270*mm, f"IFSC: {ifsc}")
            
            # Table Header
            can.setLineWidth(0.2)
            can.line(15*mm, 240*mm, 195*mm, 240*mm)
            can.setFont("Helvetica-Bold", 7.5)
            can.drawString(17*mm, 236*mm, "#")
            can.drawString(25*mm, 236*mm, "Date")
            can.drawString(50*mm, 236*mm, "Description")
            can.drawString(110*mm, 236*mm, "Chq/Ref No.")
            can.drawRightString(145*mm, 236*mm, "Withdrawal")
            can.drawRightString(170*mm, 236*mm, "Deposit")
            can.drawRightString(192*mm, 236*mm, "Balance")
            can.line(15*mm, 233*mm, 195*mm, 233*mm)
            return 228*mm

        y = draw_kotak_template(c, 1)
        c.setFont("Helvetica", 7)
        for i, row in enumerate(st.session_state.kotak_6m, 1):
            c.drawString(17*mm, y, str(i))
            c.drawString(25*mm, y, row['d'])
            c.drawString(50*mm, y, row['desc'][:35])
            c.drawString(110*mm, y, row['ref'])
            if row['wit'] > 0: c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(170*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 6*mm
            if y < 30*mm:
                c.showPage()
                y = draw_kotak_template(c, 2)
                c.setFont("Helvetica", 7)

        # Footer Narrations (Kotak Special)
        c.setFont("Helvetica-Oblique", 6)
        c.drawString(20*mm, 15*mm, "Commonly Used Narrations: UPI-Unified Payment Interface, CMS-Cash Management Service")
        
        c.save()
        
        # Final Byte Fix
        final_pdf = buf.getvalue().replace(b"ReportLab", b"OpenPDF")
        st.download_button("📥 Get Original Kotak PDF", final_pdf, "Kotak_Statement.pdf")
