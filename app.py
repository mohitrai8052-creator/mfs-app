import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from pypdf import PdfReader, PdfWriter
import random
from datetime import datetime, timedelta
import io

# --- 1. DATA GENERATOR (6 Months: April to Oct) ---
def get_6month_data(opening_bal, salary_text):
    transactions = []
    current_bal = opening_bal
    # Start Date: 7 April 2025 | End Date: 6 Oct 2025
    curr_date = datetime(2025, 10, 6, 11, 0)
    end_date = datetime(2025, 4, 7, 10, 0)
    
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        # Salary Logic (Month ki starting mein)
        if curr_date.day in [5, 6, 7] and random.random() > 0.8:
            desc, dep, wit = salary_text, 80000.0, 0.0
        else:
            ref = str(random.randint(100000000000, 999999999999))
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(100, 5000)
            
        current_bal = current_bal + dep - wit
        transactions.append({"d": d_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
        curr_date -= timedelta(hours=random.randint(18, 48))
    return transactions

# --- 2. STREAMLIT UI ---
st.set_page_config(page_title="SBI Statement System", layout="wide")
st.title("🏦 SBI Original Statement Generator")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Account Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Account Number", "00000031144336469")
with col2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFS Code", "SBIN0030082")
    cif = st.text_input("CIF No.", "85774527603")
    op_bal = st.number_input("Opening Balance (as on 7 April)", value=42.37)

if st.button("🚀 Step 1: Generate 6-Month Data"):
    st.session_state.sbi_data = get_6month_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success(f"Generated {len(st.session_state.sbi_data)} transactions!")

# --- 3. PDF GENERATION WITH PROPERTY FIX ---
if "sbi_data" in st.session_state:
    if st.button("📥 Step 2: Download Verified PDF"):
        # A. Create PDF with ReportLab
        temp_buf = io.BytesIO()
        c = canvas.Canvas(temp_buf, pagesize=A4)
        c.setPDFVersion(1, 4) # Bank standard v1.4

        def draw_page_header(can):
            can.setFont("Helvetica-Bold", 18)
            can.drawString(20*mm, 282*mm, "SBI")
            can.setFont("Courier", 8.2)
            # Header Layout
            can.drawString(20*mm, 272*mm, f"Account Name   : {name}")
            can.drawString(115*mm, 272*mm, f"Account Number : {acc}")
            can.drawString(20*mm, 267*mm, f"Address        : {addr.splitlines()[0]}")
            can.drawString(115*mm, 267*mm, f"Branch         : {branch}")
            can.drawString(20*mm, 245*mm, "Date           : 6 Oct 2025")
            can.drawString(115*mm, 255*mm, f"IFS Code       : {ifsc}")
            
            can.setFont("Courier-Bold", 9)
            can.drawString(20*mm, 232*mm, "Account Statement from 7 Apr 2025 to 6 Oct 2025")
            
            # Lines & Table Header
            can.setLineWidth(0.1)
            can.line(18*mm, 227*mm, 195*mm, 227*mm)
            can.setFont("Courier-Bold", 7.5)
            can.drawString(20*mm, 223*mm, "Txn Date")
            can.drawString(42*mm, 223*mm, "Value Date")
            can.drawString(68*mm, 223*mm, "Description")
            can.drawRightString(148*mm, 223*mm, "Debit")
            can.drawRightString(170*mm, 223*mm, "Credit")
            can.drawRightString(192*mm, 223*mm, "Balance")
            can.line(18*mm, 220*mm, 195*mm, 220*mm)
            return 215*mm

        y = draw_page_header(c)
        c.setFont("Courier", 7)
        
        for row in st.session_state.sbi_data:
            c.drawString(20*mm, y, row['d'])
            c.drawString(42*mm, y, row['d'])
            c.drawString(68*mm, y, row['desc'][:55])
            if row['wit'] > 0: c.drawRightString(148*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(170*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 4.2*mm
            if y < 20*mm:
                c.showPage()
                y = draw_page_header(c)
                c.setFont("Courier", 7)
        c.save()

        # B. Metadata Surgery with PyPDF
        temp_buf.seek(0)
        reader = PdfReader(temp_buf)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        # Injected Bank Properties
        writer.add_metadata({
            "/Producer": "iText 2.1.7 by 1T3XT",
            "/Creator": "iText 2.1.7 by 1T3XT",
            "/Author": "State Bank of India",
            "/Title": "Account Statement"
        })

        final_buf = io.BytesIO()
        writer.write(final_buf)
        
        # C. Final Byte Cleaning
        final_pdf = final_buf.getvalue()
        final_pdf = final_pdf.replace(b"ReportLab", b"iText") # Hidden traces mita do

        st.download_button("📥 Download Official iText PDF", final_pdf, "SBI_Statement_Final.pdf")
