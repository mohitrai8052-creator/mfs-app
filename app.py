import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Axis Statement Official", layout="wide")

def generate_axis_data(start_bal, salary_text):
    data = []
    current_bal = start_bal
    date_direct = datetime(2026, 2, 8) 
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        if i % 30 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        elif random.random() < 0.15:
            desc, dep, wit = "TRF FROM AXIS BANK", random.uniform(2000, 20000), 0.0
        else:
            desc, dep, wit = random.choice(["UPI/Mobikwik/9109695959", "ATM CASH WDL", "FUEL/BPCL", "VMT-ICON/9109695959", "PUR/AMAZON"]), 0.0, random.uniform(100, 5000)
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

st.title("🏦 Axis Bank Official Statement Generator")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Customer Name", "Mohit Kumar Rai")
    cust_id = st.text_input("Customer ID", "976307289")
    acc_no = st.text_input("Account Number", "925010033967742")
with col2:
    ifsc = st.text_input("IFSC Code", "UTIB0001306")
    micr = st.text_input("MICR Code", "395211007")
    opening_bal = st.number_input("Opening Balance", value=150000.0)

salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")

if st.button("🚀 STEP 1: GENERATE DATA"):
    st.session_state.axis_data = generate_axis_data(opening_bal, salary_input)
    st.success("Data ready!")

if "axis_data" in st.session_state:
    if st.button("📥 STEP 2: DOWNLOAD FINAL PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # Axis Header (Maroon)
        pdf.set_text_color(151, 27, 47) 
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "AXIS BANK", 0, 1, 'L')
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", '', 8)
        pdf.cell(0, 4, f"Customer ID: {cust_id}", 0, 1, 'L')
        pdf.cell(0, 4, f"IFSC Code: {ifsc}", 0, 1, 'L')
        pdf.cell(0, 4, f"MICR Code : {micr}", 0, 1, 'L')
        pdf.ln(5)
        
        pdf.set_font("Helvetica", 'B', 10)
        pdf.cell(0, 6, f"Statement of Axis Account No : {acc_no}", 0, 1, 'L')
        pdf.set_font("Helvetica", '', 8)
        pdf.cell(0, 5, f"Account Holder: {name}", 0, 1, 'L')
        pdf.ln(5)
        
        # TABLE HEADER (Strict Alignment)
        pdf.set_fill_color(151, 27, 47) 
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", 'B', 8)
        # Width settings: 25, 20, 75, 25, 25, 25
        pdf.cell(25, 8, "Tran Date", 1, 0, 'C', True)
        pdf.cell(20, 8, "Chq No", 1, 0, 'C', True)
        pdf.cell(70, 8, "Particulars", 1, 0, 'C', True)
        pdf.cell(25, 8, "Debit", 1, 0, 'C', True)
        pdf.cell(25, 8, "Credit", 1, 0, 'C', True)
        pdf.cell(25, 8, "Balance", 1, 1, 'C', True)
        
        # DATA ROWS
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", '', 7)
        for row in st.session_state.axis_data:
            pdf.cell(25, 6, row['date'], 1, 0, 'C')
            pdf.cell(20, 6, "", 1)
            pdf.cell(70, 6, str(row['desc'])[:45], 1)
            pdf.cell(25, 6, f"{row['wit']:,.2f}" if row['wit']>0 else "0.00", 1, 0, 'R')
            pdf.cell(25, 6, f"{row['dep']:,.2f}" if row['dep']>0 else "0.00", 1, 0, 'R')
            pdf.cell(25, 6, f"{row['bal']:,.2f}", 1, 1, 'R')
        
        pdf.ln(10)
        pdf.set_font("Helvetica", 'I', 7)
        pdf.cell(0, 5, "This is a system generated output and requires no signature.", 0, 1, 'C')
        pdf.cell(0, 5, "++++ End of Statement ++++", 0, 1, 'C')
            
        pdf.output("Axis_Final_Pro.pdf")
        with open("Axis_Final_Pro.pdf", "rb") as f:
            st.download_button("Download Now", f, file_name="Axis_Official_Statement.pdf")
            
