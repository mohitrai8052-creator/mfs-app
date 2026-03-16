import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="MFS Professional", layout="wide")

# 1. Logic with Custom Narration
def generate_auto_data(start_bal, custom_narrations, salary_text):
    data = []
    current_bal = start_bal
    date_direct = datetime(2026, 3, 1)
    
    # Narration list ko saaf karna
    narr_list = [n.strip() for n in custom_narrations.split(",")]
    
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        
        # Monthly Salary
        if i % 30 == 0:
            desc = salary_text
            dep = 80000.0
            wit = 0.0
        # 20% Inward/Credit
        elif random.random() < 0.20: 
            desc = random.choice(["UPI/Received", "CASH DEP", "INT.CREDIT", "TRF INWARD"])
            dep = random.uniform(500, 10000)
            wit = 0.0
        # 80% Outward (Custom Narrations use honge)
        else:
            desc = random.choice(narr_list)
            dep = 0.0
            wit = random.uniform(100, 5000)
            
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

# 2. UI
st.title("🏦 Mohit Financial Services")
st.subheader("Professional Custom Statement")

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

# --- Naya Narration Section ---
st.write("### ✍️ Narration Setting")
salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")
custom_input = st.text_area("Other Narrations (Comma se alag karein)", 
                            "UPI/Mobikwik/9109695959, ATM CASH WDL, FUEL/BPCL, SHOPPING/AMAZON, LOAN EMI")

if st.button("🚀 Generate Custom Statement"):
    st.session_state.auto_data = generate_auto_data(opening_bal, custom_input, salary_input)
    st.success("Aapki di hui narration ke saath data taiyar hai!")

# 3. PDF Function
if "auto_data" in st.session_state:
    if st.button("📥 Download Final PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"{bank_name}", 0, 1, 'L')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 5, f"Branch: {branch} | IFSC: {ifsc}", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(95, 8, f"Account Holder: {name}", 1, 0, 'L', True)
        pdf.cell(95, 8, f"Account No: {acc_no}", 1, 1, 'L', True)
        pdf.ln(5)
        
        pdf.set_fill_color(50, 50, 50)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(25, 10, "Date", 1, 0, 'C', True)
        pdf.cell(85, 10, "Narration", 1, 0, 'C', True)
        pdf.cell(25, 10, "Withdrawal", 1, 0, 'C', True)
        pdf.cell(25, 10, "Deposit", 1, 0, 'C', True)
        pdf.cell(30, 10, "Balance", 1, 1, 'C', True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 8)
        for row in st.session_state.auto_data:
            pdf.cell(25, 7, row['date'], 1)
            pdf.cell(85, 7, str(row['desc'])[:45], 1)
            pdf.cell(25, 7, f"{row['wit']:,.2f}" if row['wit']>0 else "0.00", 1, 0, 'R')
            pdf.cell(25, 7, f"{row['dep']:,.2f}" if row['dep']>0 else "0.00", 1, 0, 'R')
            pdf.cell(30, 7, f"{row['bal']:,.2f}", 1, 1, 'R')
            
        pdf.output("mfs_final.pdf")
        with open("mfs_final.pdf", "rb") as f:
            st.download_button("Download PDF Now", f, file_name="Statement_Custom.pdf")
            
