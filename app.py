import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="MFS Axis Pro", layout="wide")

# 1. Axis Bank Style Data Generator
def generate_axis_data(start_bal, salary_text):
    data = []
    current_bal = start_bal
    date_direct = datetime(2026, 2, 8) # Aapke PDF ki date ke hisaab se
    
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        
        if i % 30 == 0:
            desc = salary_text
            dep, wit = 80000.0, 0.0
        elif random.random() < 0.15:
            desc = random.choice(["TRF FROM FRIEND", "UPI/Received", "INT.CREDIT"])
            dep, wit = random.uniform(1000, 10000), 0.0
        else:
            desc = random.choice(["UPI/Mobikwik/9109695959", "ATM CASH WDL", "FUEL/BPCL", "VMT-ICON/Transfer", "PUR/Amazon"])
            dep, wit = 0.0, random.uniform(200, 5000)
            
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

# 2. UI Layout
st.title("🏦 Mohit Financial Services")
st.subheader("Axis Bank Professional Layout")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Account Holder Name", "Mohit Kumar Rai")
    cust_id = st.text_input("Customer ID", "976307289")
    acc_no = st.text_input("Account Number", "92501003396XXXX")
with col2:
    ifsc = st.text_input("IFSC Code", "UTIB0001306")
    micr = st.text_input("MICR Code", "395211007")
    opening_bal = st.number_input("Opening Balance", value=100000.0)

salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")

if st.button("🚀 Generate Axis Style Data"):
    st.session_state.axis_data = generate_axis_data(opening_bal, salary_input)
    st.success("Data Axis Bank format mein taiyar hai!")

# 3. PDF Generation (As per Axis Layout)
if "axis_data" in st.session_state:
    if st.button("📥 Download Axis Bank PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # Axis Header
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 8, "AXIS BANK", 0, 1, 'L')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, f"Customer ID: {cust_id}", 0, 1, 'L')
        pdf.cell(0, 5, f"IFSC Code: {ifsc}", 0, 1, 'L')
        pdf.cell(0, 5, f"MICR Code: {micr}", 0, 1, 'L')
        pdf.ln(5)
        
        # Account Name & Period
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, f"Statement of Axis Account No : {acc_no}", 0, 1, 'L')
        pdf.set_font("Arial", '', 9)
        pdf.cell(0, 5, f"Account Holder: {name}", 0, 1, 'L')
        pdf.ln(5)
        
        # Axis Table Header
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 8)
        pdf.cell(22, 10, "Tran Date", 1, 0, 'C', True)
        pdf.cell(15, 10, "Chq No", 1, 0, 'C', True)
        pdf.cell(75, 10, "Particulars", 1, 0, 'C', True)
        pdf.cell(25, 10, "Debit", 1, 0, 'C', True)
        pdf.cell(25, 10, "Credit", 1, 0, 'C', True)
        pdf.cell(28, 10, "Balance", 1, 1, 'C', True)
        
        # Table Rows
        pdf.set_font("Arial", '', 7)
        for row in st.session_state.axis_data:
            pdf.cell(22, 7, row['date'], 1)
            pdf.cell(15, 7, "", 1) # Chq No khali
            pdf.cell(75, 7, str(row['desc'])[:48], 1)
            pdf.cell(25, 7, f"{row['wit']:,.2f}" if row['wit']>0 else "", 1, 0, 'R')
            pdf.cell(25, 7, f"{row['dep']:,.2f}" if row['dep']>0 else "", 1, 0, 'R')
            pdf.cell(28, 7, f"{row['bal']:,.2f}", 1, 1, 'R')
            
        pdf.output("axis_statement.pdf")
        with open("axis_statement.pdf", "rb") as f:
            st.download_button("Save Axis Statement", f, file_name="Axis_Statement.pdf")
