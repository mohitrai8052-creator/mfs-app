import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
from datetime import datetime, timedelta
import io

# --- 1. Authentic Kotak Data Generator (6 Months) ---
def get_kotak_6m_data(op_bal):
    data = []
    curr_bal = op_bal
    # Current Date se piche 6 mahine
    curr_date = datetime(2026, 3, 18)
    end_date = datetime(2025, 9, 18)
    
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        ref_no = f"UPI-{random.randint(600000000000, 699999999999)}"
        
        # Monthly Salary Logic
        if curr_date.day in [1, 2, 3, 4, 5] and random.random() > 0.8:
            desc = "CMS-SALARY/TATA MOTORS LTD"
            dep, wit = 75000.0, 0.0
        else:
            desc = f"UPI/PAYMENT/{random.randint(1000, 9999)}/Purchase"
            dep, wit = 0.0, random.uniform(50, 5000)
            
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "ref": ref_no, "wit": wit, "dep": dep, "bal": curr_bal})
        curr_date -= timedelta(hours=random.randint(18, 48))
    return data

st.title("🏦 Kotak Bank Original Properties Fixer")

# Inputs
name = st.text_input("Customer Name", "Girase Vinod Rajusing")
acc_no = st.text_input("Account No.", "9748659761")
op_bal = st.number_input("Opening Balance (as on 18 Sep 2025)", value=201.87)

if st.button("🚀 Step 1: Fix All Data"):
    st.session_state.kotak_master_data = get_kotak_6m_data(op_bal)
    st.success("Data Ready! Now applying OpenPDF 2.0.3 Surgery...")

if "kotak_master_data" in st.session_state:
    if st.button("📥 Step 2: Download Verified PDF"):
        buf = io.BytesIO()
        # Compression=0 is mandatory to keep the binary text readable for replacement
        c = canvas.Canvas(buf, pagesize=A4, pageCompression=0)
        c.setPDFVersion(1, 5) # Kotak standard

        def draw_kotak_header(can):
            can.setFont("Helvetica-Bold", 14)
            can.drawString(20*mm, 280*mm, "kotak")
            can.setFont("Helvetica", 8)
            can.drawString(20*mm, 270*mm, f"Account No: {acc_no}")
            can.drawString(20*mm, 265*mm, f"Customer Name: {name}")
            can.line(15*mm, 240*mm, 195*mm, 240*mm)
            return 230*mm

        y = draw_kotak_header(c)
        c.setFont("Helvetica", 7)
        for row in st.session_state.kotak_master_data:
            c.drawString(20*mm, y, row['d'])
            c.drawString(45*mm, y, row['desc'][:50])
            if row['wit'] > 0: c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(170*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 6*mm
            if y < 25*mm:
                c.showPage()
                y = draw_kotak_header(c)
                c.setFont("Helvetica", 7)
        c.save()

        # --- THE MASTER BINARY FIX ---
        raw_pdf_bytes = buf.getvalue()
        
        # 1. Producer & Creator Fix
        raw_pdf_bytes = raw_pdf_bytes.replace(b"ReportLab PDF Library - www.reportlab.com", b"OpenPDF 2.0.3")
        raw_pdf_bytes = raw_pdf_bytes.replace(b"ReportLab", b"OpenPDF")
        raw_pdf_bytes = raw_pdf_bytes.replace(b"reportlab.com", b"kotak.com")
        
        # 2. XMP Metadata Block Fix (Forcefully hiding library name)
        raw_pdf_bytes = raw_pdf_bytes.replace(b"<pdf:Producer>iText", b"<pdf:Producer>OpenPDF 2.0.3")
        
        st.download_button("📥 Download Property-Locked PDF", raw_pdf_bytes, "Kotak_Statement.pdf")
