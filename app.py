import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Axis Statement Pro", layout="wide")

def generate_axis_data(start_bal, salary_text):
    data = []
    current_bal = start_bal
    # [span_4](start_span)Aapke PDF ki last date 08-02-2026 hai[span_4](end_span)
    date_direct = datetime(2026, 2, 8) 
    
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        if i % 30 == 0:
            desc = salary_text
            dep, wit = 80000.0, 0.0
        elif random.random() < 0.20:
            desc = random.choice(["UPI/Received/Friend", "TRF FROM AXIS/MFS", "INT.CREDIT"])
            dep, wit = random.uniform(500, 15000), 0.0
        else:
            desc = random.choice(["UPI/Mobikwik/9109695959", "ATM CASH WDL", "FUEL/BPCL", "VMT-ICON/Transfer", "PUR/Amazon"])
            dep, wit = 0.0, random.uniform(100, 6000)
            
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

st.title("🏦 Axis Bank Statement Generator")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", "Mohit Kumar Rai")
    cust_id = st.text_input("Customer ID", "976307289")
    acc_no = st.text_input("Account No", "925010033967742")
with col2:
    ifsc = st.text_input("IFSC", "UTIB0001306")
    micr = st.text_input("MICR", "395211007")
    opening_bal = st.number_input("Opening Bal", value=100000.0)

salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")

if st.button("🚀 Step 1: Generate Balanced Data"):
    st.session_state.axis_data = generate_axis_data(opening_bal, salary_input)
    st.success("Data Generated!")

if "axis_data" in st.session_state:
    if st.button("📥 Step 2: Download Axis Style PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # [span_5](start_span)Axis Bank Header[span_5](end_span)
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, "AXIS BANK", 0, 1, 'L')
        pdf.set_font("Helvetica", '', 8)
        pdf.cell(0, 4, f"Customer ID: {cust_id}", 0, 1, 'L')
        pdf.cell(0, 4, f"IFSC Code: {ifsc}", 0, 1, 'L')
        pdf.cell(0, 4, f"MICR Code : {micr}", 0, 1, 'L')
        pdf.ln(4)
        
        pdf.set_font("Helvetica", 'B', 9)
        pdf.cell(0, 6, f"Statement of Axis Account No : {acc_no} for the period", 0, 1, 'L')
        pdf.set_font("Helvetica", '', 8)
        pdf.cell(0, 5, f"Account Holder: {name}", 0, 1, 'L')
        pdf.ln(5)
        
        # [span_6](start_span)Table Header[span_6](end_span)
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Helvetica", 'B', 8)
        pdf.cell(22, 8, "Tran Date", 1, 0, 'C', True)
        pdf.cell(15, 8, "Chq No", 1, 0, 'C', True)
        pdf.cell(80, 8, "Particulars", 1, 0, 'C', True)
        pdf.cell(24, 8, "Debit", 1, 0, 'C', True)
        pdf.cell(24, 8, "Credit", 1, 0, 'C', True)
        pdf.cell(25, 8, "Balance", 1, 1, 'C', True)
        
        # [span_7](start_span)Table Rows[span_7](end_span)
        pdf.set_font("Helvetica", '', 7)
        for row in st.session_state.axis_data:
            pdf.cell(22, 6, row['date'], 1, 0, 'C')
            pdf.cell(15, 6, "", 1)
            pdf.cell(80, 6, str(row['desc'])[:50], 1)
            pdf.cell(24, 6, f"{row['wit']:,.2f}" if row['wit']>0 else "", 1, 0, 'R')
            pdf.cell(24, 6, f"{row['dep']:,.2f}" if row['dep']>0 else "", 1, 0, 'R')
            pdf.cell(25, 6, f"{row['bal']:,.2f}", 1, 1, 'R')
            
        pdf.output("axis_pro.pdf")
        with open("axis_pro.pdf", "rb") as f:
            st.download_button("Final Download", f, file_name="Axis_Statement_Final.pdf")
