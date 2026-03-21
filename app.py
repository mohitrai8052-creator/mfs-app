import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from pypdf import PdfReader, PdfWriter
import random
from datetime import datetime, timedelta
import io

# 1. Authentic Data Generator
def get_sbi_data(op_bal, sal_text):
    data = []
    curr_bal = op_bal
    curr_date = datetime(2025, 10, 6, 11, 0)
    end_date = datetime(2025, 4, 7, 10, 0)
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        if curr_date.day in [5, 6, 7] and random.random() > 0.8:
            desc, dep, wit = sal_text, 80000.0, 0.0
        else:
            ref = str(random.randint(100000000000, 999999999999))
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(50, 4500)
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "wit": wit, "dep": dep, "bal": curr_bal})
        curr_date -= timedelta(hours=random.randint(12, 40))
    return data

st.title("🏦 SBI Original Property - XMP Wipe Version")

# Inputs
name = st.text_input("Account Name", "Mr. ASHISH TIWARI")
acc = st.text_input("Account Number", "00000031144336469")
op_bal = st.number_input("Opening Balance (7 Apr)", value=42.37)

if st.button("🚀 Step 1: Fix Data"):
    st.session_state.master_v18 = get_sbi_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success("Data Ready! Deep cleaning metadata...")

if "master_v18" in st.session_state:
    if st.button("📥 Step 2: Download Verified PDF"):
        # A. Create PDF with ReportLab
        temp_buf = io.BytesIO()
        c = canvas.Canvas(temp_buf, pagesize=A4, pageCompression=0)
        c.setPDFVersion(1, 4)
        
        def draw_template(can):
            can.setFont("Helvetica-Bold", 16)
            can.drawString(20*mm, 282*mm, "SBI")
            can.setFont("Courier", 8.2)
            can.drawString(20*mm, 272*mm, f"Account Name   : {name}")
            can.drawString(115*mm, 272*mm, f"Account Number : {acc}")
            can.setFont("Courier-Bold", 9)
            can.drawString(20*mm, 232*mm, "Account Statement from 7 Apr 2025 to 6 Oct 2025")
            can.setLineWidth(0.1)
            can.line(18*mm, 227*mm, 195*mm, 227*mm)
            can.setFont("Courier-Bold", 7.5)
            can.drawString(20*mm, 223*mm, "Txn Date")
            can.drawString(68*mm, 223*mm, "Description")
            can.drawRightString(192*mm, 223*mm, "Balance")
            can.line(18*mm, 220*mm, 195*mm, 220*mm)
            return 215*mm

        y = draw_template(c)
        c.setFont("Courier", 7)
        for row in st.session_state.master_v18:
            c.drawString(20*mm, y, row['d'])
            c.drawString(68*mm, y, row['desc'][:58])
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 4.2*mm
            if y < 20*mm:
                c.showPage()
                y = draw_template(c)
                c.setFont("Courier", 7)
        c.save()

        # B. Metadata Surgery using PyPDF (Cleaning XMP)
        temp_buf.seek(0)
        reader = PdfReader(temp_buf)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # XMP Metadata ko 'None' karke purani branding hatana
        writer.xmp_metadata = None 

        # Nayi Bank Properties add karna
        writer.add_metadata({
            "/Producer": "iText 2.1.7 by 1T3XT",
            "/Creator": "iText 2.1.7 by 1T3XT",
            "/Author": "State Bank of India",
            "/Title": "Account Statement"
        })

        final_buf = io.BytesIO()
        writer.write(final_buf)
        
        # C. Final Binary Fix (Replacing any leftover strings)
        pdf_data = final_buf.getvalue()
        pdf_data = pdf_data.replace(b"ReportLab", b"iText")
        pdf_data = pdf_data.replace(b"reportlab.com", b"sbi.co.in")

        st.download_button("📥 Download Official iText PDF", pdf_data, "SBI_Statement.pdf")
