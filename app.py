import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta
import io

# --- 1. Authentic Kotak Data ---
def get_kotak_6m_data(op_bal):
    data = []
    curr_bal = op_bal
    curr_date = datetime(2026, 3, 18)
    for i in range(1, 100):
        d_str = curr_date.strftime("%d %b %Y")
        ref = f"UPI-{random.randint(600000000000, 699999999999)}"
        if random.random() > 0.85:
            desc, dep, wit = "CMS-SALARY/TATA MOTORS", 75000.0, 0.0
        else:
            desc, dep, wit = "UPI/PAYMENT/MERCHANT", 0.0, random.uniform(20, 3000)
        curr_bal = curr_bal + dep - wit
        data.append([str(i), d_str, desc, ref, f"{wit:.2f}" if wit > 0 else "", f"{dep:.2f}" if dep > 0 else "", f"{curr_bal:.2f}"])
        curr_date -= timedelta(hours=random.randint(20, 50))
    return data

st.title("🏦 Kotak Bank - Ultimate Property Fixer")

name = st.text_input("Name", "Girase Vinod Rajusing")
acc = st.text_input("Account No.", "9748659761")

if st.button("🚀 Step 1: Generate Data"):
    st.session_state.k_data = get_kotak_6m_data(201.87)
    st.success("Data Ready!")

if "k_data" in st.session_state:
    if st.button("📥 Step 2: Download OpenPDF Verified Statement"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # --- METADATA FIX ---
        pdf.set_author("Kotak Mahindra Bank")
        pdf.set_creator("OpenPDF 2.0.3")
        pdf.set_title("Account Statement")
        
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "kotak", 0, 1)
        
        pdf.set_font("Arial", size=8)
        pdf.cell(0, 5, f"Account No: {acc}", 0, 1)
        pdf.cell(0, 5, f"Customer Name: {name}", 0, 1)
        pdf.ln(10)
        
        # Header
        pdf.set_font("Arial", 'B', 7)
        cols = ["#", "Date", "Description", "Ref No.", "Withdrawal", "Deposit", "Balance"]
        widths = [10, 25, 60, 35, 20, 20, 20]
        for i in range(len(cols)):
            pdf.cell(widths[i], 7, cols[i], 1)
        pdf.ln()
        
        # Data
        pdf.set_font("Arial", size=7)
        for row in st.session_state.k_data:
            for i in range(len(row)):
                pdf.cell(widths[i], 6, row[i], 1)
            pdf.ln()
            
        # --- THE MASTER HACK ---
        # FPDF metadata binary replacement
        raw_pdf = pdf.output(dest='S')
        if isinstance(raw_pdf, str):
            raw_pdf = raw_pdf.encode('latin1')
            
        # Force Injecting Producer
        final_pdf = raw_pdf.replace(b"/Producer (FPDF 1.86)", b"/Producer (OpenPDF 2.0.3)")
        final_pdf = final_pdf.replace(b"FPDF", b"OpenPDF")
        
        st.download_button("📥 Get Verified PDF", final_pdf, "Kotak_Statement.pdf")
