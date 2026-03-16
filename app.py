import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="MFS Professional", layout="wide")

# 1. Improved Logic: Mix of Credits and Debits
def generate_auto_data(start_bal):
    data = []
    current_bal = start_bal
    date_direct = datetime(2026, 3, 1)
    
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        
        # Har 30 din par Salary Credit
        if i % 30 == 0:
            desc = "SALARY/TATA MOTORS LTD/MAR-26"
            dep = 80000.0
            wit = 0.0
        # Randomly beech mein 20% chances hain ki paisa credit ho (UPI/Transfer)
        elif random.random() < 0.20: 
            desc = random.choice(["UPI/Received/Friend", "TRF/MFS/INWARD", "CASH DEPOSIT/SELF", "INT.CREDIT"])
            dep = random.uniform(500, 15000)
            wit = 0.0
        # Baaki 80% chances Debits ke hain
        else:
            desc = random.choice(["UPI/Mobikwik/9109695959", "ATM CASH WDL", "FUEL/BPCL", "UPI/ZOMATO", "EMI/AUTO-DEBIT"])
            dep = 0.0
            wit = random.uniform(100, 8000)
            
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

# 2. UI for User Input
st.title("🏦 Mohit Financial Services")
st.subheader("Professional Bank Statement System")

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

if st.button("🚀 Step 1: Generate Balanced Statement"):
    st.session_state.auto_data = generate_auto_data(opening_bal)
    st.success("Data balanced ho gaya hai! Credits aur Debits dono mix hain.")

# 3. PDF Generation
if "auto_data" in st.session_state:
    if st.button("📥 Step 2: Download Professional PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"{bank_name}", 0, 1, 'L')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, f"Branch: {branch} | IFSC: {ifsc}", 0, 1, 'L')
        pdf.ln(5)
        
        # Customer Box
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(95, 8, f"Account Holder: {name}", 1, 0, 'L', True)
        pdf.cell(95, 8, f"Account No: {acc_no}", 1, 1, 'L', True)
        pdf.ln(5)
        
        # Table Header
        pdf.set_fill_color(50, 50, 50)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(25, 10, "Date", 1, 0, 'C', True)
        pdf.cell(85, 10, "Narration", 1, 0, 'C', True)
        pdf.cell(25, 10, "Withdrawal", 1, 0, 'C', True)
        pdf.cell(25, 10, "Deposit", 1, 0, 'C', True)
        pdf.cell(30, 10, "Balance", 1, 1, 'C', True)
        
        # Data
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 8)
        for row in st.session_state.auto_data:
            pdf.cell(25, 7, row['date'], 1)
            pdf.cell(85, 7, row['desc'], 1)
            pdf.cell(25, 7, f"{row['wit']:,.2f}" if row['wit']>0 else "0.00", 1, 0, 'R')
            pdf.cell(25, 7, f"{row['dep']:,.2f}" if row['dep']>0 else "0.00", 1, 0, 'R')
            pdf.cell(30, 7, f"{row['bal']:,.2f}", 1, 1, 'R')
            
        pdf.output("balanced_statement.pdf")
        with open("balanced_statement.pdf", "rb") as f:
            st.download_button("Download Now", f, file_name="Statement_Final.pdf")
