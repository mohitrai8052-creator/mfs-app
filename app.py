import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="SBI Official Statement", layout="wide")

def generate_sbi_data(start_bal, salary_text):
    data = []
    current_bal = start_bal
    date_start = datetime(2025, 10, 6) 
    for i in range(100):
        d = date_start - timedelta(days=i)
        date_str = d.strftime("%d %b %Y")
        if i % 30 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        elif random.random() < 0.2:
            desc, dep, wit = f"BY TRANSFER-UPI/CR/{random.randint(100000000000,999999999999)}/PAYTM", random.uniform(500, 5000), 0.0
        else:
            desc, dep, wit = f"TO TRANSFER-UPI/DR/{random.randint(100000000000,999999999999)}/9109695959", 0.0, random.uniform(10, 2000)
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

st.title("🏦 SBI Official Copy Generator")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Account Name", "MOHIT KUMAR RAI")
    address = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc_no = st.text_input("Account Number", "00000031144336469")
with col2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFS Code", "SBIN0030082")
    cif = st.text_input("CIF No", "85774527603")
    opening_bal = st.number_input("Balance as on 7 Apr 2025", value=42.37)

salary_input = st.text_input("Salary Narration", "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")

if st.button("🚀 Step 1: Generate Data"):
    st.session_state.sbi_final_data = generate_sbi_data(opening_bal, salary_input)
    st.success("SBI Data Ready!")

if "sbi_final_data" in st.session_state:
    if st.button("📥 Step 2: Download SBI Statement"):
        pdf = FPDF()
        pdf.add_page()
        
        # --- SBI HEADER ---
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, "SBI", 0, 1, 'L')
        pdf.ln(2)

        # --- INFO BLOCK (Two Columns like Original) ---
        pdf.set_font("Helvetica", '', 8)
        # Left Side
        pdf.text(10, 25, f"Account Name : {name}")
        pdf.text(10, 30, "Address : ")
        pdf.set_xy(30, 27)
        pdf.multi_cell(60, 4, address)
        
        # Right Side
        pdf.text(110, 25, f"Account Number : {acc_no}")
        pdf.text(110, 30, f"Branch : {branch}")
        pdf.text(110, 35, f"IFS Code : {ifsc}")
        pdf.text(110, 40, f"CIF No : {cif}")
        
        pdf.set_xy(10, 55)
        pdf.set_font("Helvetica", 'B', 9)
        pdf.cell(0, 5, "Account Statement from 7 Apr 2025 to 6 Oct 2025", 0, 1, 'L')
        pdf.ln(2)

        # --- TABLE HEADER ---
        pdf.set_font("Helvetica", 'B', 7)
        pdf.cell(20, 7, "Txn Date", 1, 0, 'C')
        pdf.cell(20, 7, "Value Date", 1, 0, 'C')
        pdf.cell(80, 7, "Description", 1, 0, 'C')
        pdf.cell(10, 7, "Ref No.", 1, 0, 'C')
        pdf.cell(20, 7, "Debit", 1, 0, 'C')
        pdf.cell(20, 7, "Credit", 1, 0, 'C')
        pdf.cell(20, 7, "Balance", 1, 1, 'C')

        # --- DATA ---
        pdf.set_font("Helvetica", '', 6.5)
        for row in st.session_state.sbi_final_data:
            start_y = pdf.get_y()
            pdf.cell(20, 8, row['date'], 1, 0, 'C')
            pdf.cell(20, 8, row['date'], 1, 0, 'C')
            # Multi-cell for description to wrap text like original
            pdf.set_xy(50, start_y)
            pdf.multi_cell(80, 4, row['desc'], 1, 'L')
            
            pdf.set_xy(130, start_y)
            pdf.cell(10, 8, "", 1, 0)
            pdf.cell(20, 8, f"{row['wit']:,.2f}" if row['wit']>0 else "", 1, 0, 'R')
            pdf.cell(20, 8, f"{row['dep']:,.2f}" if row['dep']>0 else "", 1, 0, 'R')
            pdf.cell(20, 8, f"{row['bal']:,.2f}", 1, 1, 'R')

        pdf.ln(10)
        pdf.set_font("Helvetica", 'I', 7)
        pdf.cell(0, 5, "** This is a computer generated statement and does not require a signature.", 0, 1, 'L')
        
        pdf.output("SBI_Final.pdf")
        with open("SBI_Final.pdf", "rb") as f:
            st.download_button("Download Official SBI Statement", f, file_name="SBI_Statement.pdf")
