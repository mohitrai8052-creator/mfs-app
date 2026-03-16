import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Axis Official Statement", layout="wide")

def generate_axis_data(start_bal, salary_text):
    data = []
    current_bal = start_bal
    date_direct = datetime(2026, 2, 8) 
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        if i % 30 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        elif random.random() < 0.15:
            desc, dep, wit = "TAB-925010033967742", random.uniform(5000, 15000), 0.0
        else:
            desc, dep, wit = random.choice(["VMT-ICON/9109695959", "ATM CASH WDL", "FUEL/BPCL", "PUR/AMAZON", "UPI/9109695959"]), 0.0, random.uniform(100, 5000)
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

st.title("🏦 Axis Bank Copy Generator")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", "DNYANESHWAR RAMDAS BAVASKAR")
    address = st.text_area("Address", "GL G 3 MAHALAXMI APPARTMENT 2\nNARAYAN NAGAR SOCIETY, PUNAGAM\nSURAT, GUJARAT-395010")
    cust_id = st.text_input("Customer ID", "976307289")
with col2:
    acc_no = st.text_input("Account No", "925010033967742")
    ifsc = st.text_input("IFSC", "UTIB0001306")
    micr = st.text_input("MICR", "395211007")
    opening_bal = st.number_input("Opening Balance", value=150000.0)

salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")

if st.button("🚀 STEP 1: GENERATE DATA"):
    st.session_state.axis_data = generate_axis_data(opening_bal, salary_input)
    st.success("Data ready!")

if "axis_data" in st.session_state:
    if st.button("📥 STEP 2: DOWNLOAD CARBON COPY PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # Customer Info (Plain Text like Original)
        pdf.set_font("Helvetica", '', 9)
        pdf.multi_cell(0, 5, f"{name}\n{address}\nRegistered Mobile No: XXXXXX5959", 0, 'L')
        pdf.ln(5)
        
        # Axis Header Info
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, "AXIS BANK", 0, 1, 'R')
        pdf.set_font("Helvetica", '', 8)
        pdf.cell(0, 4, f"Customer ID: {cust_id}   IFSC Code: {ifsc}   MICR Code: {micr}", 0, 1, 'R')
        pdf.ln(5)
        
        pdf.set_font("Helvetica", 'B', 9)
        pdf.cell(0, 6, f"Statement of Axis Account No : {acc_no} for the period", 0, 1, 'L')
        pdf.ln(2)
        
        # Table Header (Clean Plain Black)
        pdf.set_font("Helvetica", 'B', 7)
        pdf.cell(20, 8, "Tran Date", 1, 0, 'C')
        pdf.cell(15, 8, "Chq No", 1, 0, 'C')
        pdf.cell(75, 8, "Particulars", 1, 0, 'C')
        pdf.cell(25, 8, "Debit", 1, 0, 'C')
        pdf.cell(25, 8, "Credit", 1, 0, 'C')
        pdf.cell(25, 8, "Balance", 1, 0, 'C')
        pdf.cell(10, 8, "Init.", 1, 1, 'C')
        
        # Rows
        pdf.set_font("Helvetica", '', 7)
        for row in st.session_state.axis_data:
            pdf.cell(20, 6, row['date'], 1, 0, 'C')
            pdf.cell(15, 6, "", 1)
            pdf.cell(75, 6, f" {row['desc']}", 1, 0, 'L')
            pdf.cell(25, 6, f"{row['wit']:,.2f}" if row['wit']>0 else "", 1, 0, 'R')
            pdf.cell(25, 6, f"{row['dep']:,.2f}" if row['dep']>0 else "", 1, 0, 'R')
            pdf.cell(25, 6, f"{row['bal']:,.2f}", 1, 0, 'R')
            pdf.cell(10, 6, "101", 1, 1, 'C')
        
        pdf.ln(10)
        pdf.set_font("Helvetica", '', 7)
        pdf.cell(0, 4, "This is a system generated output and requires no signature.", 0, 1, 'C')
        pdf.cell(0, 4, "++++ End of Statement ++++", 0, 1, 'C')
            
        pdf.output("Axis_Carbon_Copy.pdf")
        with open("Axis_Carbon_Copy.pdf", "rb") as f:
            st.download_button("Save Final PDF", f, file_name="Axis_Official_Statement.pdf")
            
