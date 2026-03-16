import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="MFS Professional", layout="wide")

# 1. Automatic Data Generator logic
def generate_auto_data(start_bal):
    data = []
    current_bal = start_bal
    date_direct = datetime(2026, 3, 1)
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        if i % 30 == 0:
            desc = "SALARY/TATA MOTORS LTD/MAR-26"
            dep, wit = 80000.0, 0.0
        else:
            desc = random.choice(["UPI/Mobikwik/9109695959", "ATM CASH WDL", "FUEL/BPCL", "MFS/TRANSFER", "UPI/ZOMATO"])
            dep, wit = 0.0, random.uniform(200, 4500)
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

# 2. UI for User Input
st.title("🏦 Mohit Financial Services")
st.subheader("Bank Statement Details")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Customer Name", "Mohit Kumar Rai")
    bank_name = st.selectbox("Bank Name", ["AXIS BANK", "STATE BANK OF INDIA", "HDFC BANK"])
    acc_no = st.text_input("Account Number", "9210200XXXX5959")
with col2:
    ifsc = st.text_input("IFSC Code", "UTIB0001234")
    branch = st.text_input("Branch Name", "Jabalpur Branch")
    opening_bal = st.number_input("Opening Balance", value=100000.0)

st.divider()

if st.button("🚀 Step 1: Generate 150 Entries (6 Months)"):
    st.session_state.auto_data = generate_auto_data(opening_bal)
    st.success("Data ready ho gaya hai!")

# 3. PDF Generation with Account Details
if "auto_data" in st.session_state:
    if st.button("📥 Step 2: Download Professional PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # Professional Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"{bank_name}", 0, 1, 'L')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, f"Branch: {branch} | IFSC: {ifsc}", 0, 1, 'L')
        pdf.ln(5)
        
        # Account Info Table
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(95, 8, f"Account Holder: {name}", 1, 0, 'L', True)
        pdf.cell(95, 8, f"Account No: {acc_no}", 1, 1, 'L', True)
        pdf.ln(5)
        
        # Transaction Table Header
        pdf.set_fill_color(50, 50, 50)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(25, 10, "Date", 1, 0, 'C', True)
        pdf.cell(85, 10, "Narration", 1, 0, 'C', True)
        pdf.cell(25, 10, "Withdrawal", 1, 0, 'C', True)
        pdf.cell(25, 10, "Deposit", 1, 0, 'C', True)
        pdf.cell(30, 10, "Balance", 1, 1, 'C', True)
        
        # Table Rows
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 8)
        for row in st.session_state.auto_data:
            pdf.cell(25, 7, row['date'], 1)
            pdf.cell(85, 7, row['desc'], 1)
            pdf.cell(25, 7, f"{row['wit']:.2f}" if row['wit']>0 else "0.00", 1, 0, 'R')
            pdf.cell(25, 7, f"{row['dep']:.2f}" if row['dep']>0 else "0.00", 1, 0, 'R')
            pdf.cell(30, 7, f"{row['bal']:.2f}", 1, 1, 'R')
            
        pdf.output("mfs_bank_statement.pdf")
        with open("mfs_bank_statement.pdf", "rb") as f:
            st.download_button("Click here to Download PDF", f, file_name="Statement.pdf")
            
