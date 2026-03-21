import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from pypdf import PdfReader, PdfWriter
import random
from datetime import datetime, timedelta
import io

# --- 1. Authentic Kotak Data Generator (6 Months) ---
def get_kotak_6m_data(op_bal):
    data = []
    curr_bal = op_bal
    curr_date = datetime(2026, 3, 18)
    end_date = datetime(2025, 9, 18)
    
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        ref_no = f"UPI-{random.randint(600000000000, 699999999999)}"
        
        if curr_date.day in [1, 2, 3] and random.random() > 0.7:
            desc = "CMS-SALARY/TATA MOTORS LTD"
            dep, wit = 75000.0, 0.0
        else:
            desc = f"UPI/PAYMENT/{random.randint(1000, 9999)}/Purchase"
            dep, wit = 0.0, random.uniform(50, 5000)
            
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "ref": ref_no, "wit": wit, "dep": dep, "bal": curr_bal})
        curr_date -= timedelta(hours=random.randint(15, 45))
    return data

st.title("🏦 Kotak Original Properties - Atomic Fix")

# Inputs
name = st.text_input("Customer Name", "Girase Vinod Rajusing")
acc_no = st.text_input("Account No.", "9748659761")
op_bal = st.number_input("Opening Balance", value=201.87)

if st.button("🚀 Step 1: Prepare 6-Month Data"):
    st.session_state.kotak_final_data = get_kotak_6m_data(op_bal)
    st.success("Data Generated! Ready for Metadata Surgery.")

if "kotak_final_data" in st.session_state:
    if st.button("📥 Step 2: Download Verified PDF"):
        # A. Create PDF with Compression OFF
        temp_buf = io.BytesIO()
        c = canvas.Canvas(temp_buf, pagesize=A4, pageCompression=0)
        c.setPDFVersion(1, 5) # Matches Kotak's 1.5 Version

        def draw_header(can):
            can.setFont("Helvetica-Bold", 14)
            can.drawString(20*mm, 280*mm, "kotak")
            can.setFont("Helvetica", 8)
            can.drawString(20*mm, 270*mm, f"Account No: {acc_no}")
            can.drawString(20*mm, 265*mm, f"Customer Name: {name}")
            can.line(15*mm, 240*mm, 195*mm, 240*mm)
            return 230*mm

        y = draw_header(c)
        c.setFont("Helvetica", 7)
        for i, row in enumerate(st.session_state.kotak_final_data, 1):
            c.drawString(20*mm, y, row['d'])
            c.drawString(45*mm, y, row['desc'][:45])
            if row['wit'] > 0: c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(170*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 6*mm
            if y < 25*mm:
                c.showPage()
                y = draw_header(c)
                c.setFont("Helvetica", 7)
        c.save()

        # B. METADATA SURGERY (The Fix)
        temp_buf.seek(0)
        reader = PdfReader(temp_buf)
        writer = PdfWriter()
        
        # Copy pages to a new writer (This drops ReportLab's hidden info block)
        for page in reader.pages:
            writer.add_page(page)

        # Force Injecting Kotak's Original Metadata
        writer.add_metadata({
            "/Producer": "OpenPDF 2.0.3",
            "/Creator": "OpenPDF 2.0.3",
            "/Author": "Kotak Mahindra Bank",
            "/Title": "Account Statement",
            "/CreationDate": "D:20260319115346Z"
        })

        final_buf = io.BytesIO()
        writer.write(final_buf)
        
        # C. Final Byte-Level Scrubbing
        final_pdf_data = final_buf.getvalue()
        # Mita do ReportLab ka har ek nishaan binary se
        final_pdf_data = final_pdf_data.replace(b"ReportLab", b"OpenPDF")
        
        st.download_button("📥 Get Verified Kotak PDF", final_pdf_data, "Kotak_Statement.pdf")
