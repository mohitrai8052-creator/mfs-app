import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Axis Statement Carbon Copy", layout="wide")

def generate_axis_data(start_bal, salary_text):
    data = []
    current_bal = start_bal
    date_direct = datetime(2026, 2, 8) 
    for i in range(150):
        date_str = (date_direct - timedelta(days=i)).strftime("%d-%m-%Y")
        if i % 30 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        elif random.random() < 0.15:
            desc, dep, wit = f"TAB-{random.randint(900000000000000, 999999999999999)}", random.uniform(5000, 15000), 0.0
        else:
            desc, dep, wit = random.choice(["VMT-ICON/9109695959", "ATM CASH WDL", "FUEL/BPCL", "PUR/AMAZON", "UPI/9109695959"]), 0.0, random.uniform(100, 5000)
        current_bal = current_bal + dep - wit
        data.append({"date": date_str, "desc": desc, "wit": wit, "dep": dep, "bal": current_bal})
    return data

st.title("🏦 Axis Bank Official Statement Generator")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Customer Name", "DNYANESHWAR RAMDAS BAVASKAR")
    address = st.text_area("Address", "GL G 3 MAHALAXMI APPARTMENT 2\nNARAYAN NAGAR SOCIETY, PUNAGAM\nSURAT, GUJARAT-395010")
    cust_id = st.text_input("Customer ID", "976307289")
with col2:
    acc_no = st.text_input("Account Number", "925010033967742")
    ifsc = st.text_input("IFSC Code", "UTIB0001306")
    micr = st.text_input("MICR Code", "395211007")
    opening_bal = st.number_input("Opening Balance", value=150000.0)

salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")

if st.button("🚀 Step 1: Taiyar karein"):
    st.session_state.axis_data = generate_axis_data(opening_bal, salary_input)
    st.success("Data ready!")

if "axis_data" in st.session_state:
    if st.button("📥 Step 2: Download Official PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # --- HEADER LOGO AREA ---
        pdf.set_fill_color(151, 27, 47) # Axis Maroon
        pdf.rect(10, 10, 40, 10, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.text(12, 17, "AXIS BANK")
        
        # --- CUSTOMER DETAILS (Left) ---
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", 'B', 10)
        pdf.set_xy(10, 25)
        pdf.cell(0, 5, name, 0, 1, 'L')
        pdf.set_font("Helvetica", '', 8)
        pdf.multi_cell(100, 4, address)
        pdf.cell(0, 5, "Registered Mobile No: XXXXXX5959", 0, 1, 'L')
        
        # --- BANK DETAILS (Right) ---
        pdf.set_xy(130, 25)
        pdf.set_font("Helvetica", '', 8)
        pdf.cell(0, 4, f"Customer ID: {cust_id}", 0, 1, 'R')
        pdf.set_x(130)
        pdf.cell(0, 4, f"IFSC Code: {ifsc}", 0, 1, 'R')
        pdf.set_x(130)
        pdf.cell(0, 4, f"MICR Code: {micr}", 0, 1, 'R')
        
        pdf.ln(10)
        pdf.set_font("Helvetica", 'B', 9)
        pdf.cell(0, 6, f"Statement of Axis Account No : {acc_no} for the period (01-09-2025 To 08-02-2026)", 0, 1, 'L')
        pdf.ln(2)
        
        # --- TABLE HEADER ---
        pdf.set_font("Helvetica", 'B', 7)
        pdf.cell(22, 7, "Tran Date", 1, 0, 'C')
        pdf.cell(18, 7, "Chq No", 1, 0, 'C')
        pdf.cell(70, 7, "Particulars", 1, 0, 'C')
        pdf.cell(25, 7, "Debit", 1, 0, 'C')
        pdf.cell(25, 7, "Credit", 1, 0, 'C')
        pdf.cell(30, 7, "Balance", 1, 1, 'C')
        
        # --- ROWS ---
        pdf.set_font("Helvetica", '', 7)
        for row in st.session_state.axis_data:
            pdf.cell(22, 6, row['date'], 1, 0, 'C')
            pdf.cell(18, 6, "", 1)
            pdf.cell(70, 6, f" {row['desc']}", 1, 0, 'L')
            pdf.cell(25, 6, f"{row['wit']:,.2f} " if row['wit']>0 else " ", 1, 0, 'R')
            pdf.cell(25, 6, f"{row['dep']:,.2f} " if row['dep']>0 else " ", 1, 0, 'R')
            pdf.cell(30, 6, f"{row['bal']:,.2f} ", 1, 1, 'R')
            
        # --- FOOTER ---
        pdf.ln(10)
        pdf.set_font("Helvetica", '', 6)
        pdf.set_text_color(120, 120, 120)
        footer = "REGISTERED OFFICE - AXIS BANK LTD, TRISHUL, Ahmedabad. 380006.\nBRANCH ADDRESS - AXIS BANK LTD, NAVAGAM [GJ], SURAT, GUJARAT."
        pdf.multi_cell(0, 4, footer, 0, 'C')
        pdf.ln(2)
        pdf.set_font("Helvetica", 'B', 7)
        pdf.cell(0, 5, "++++ End of Statement ++++", 0, 1, 'C')
            
        pdf.output("Axis_Pro_Statement.pdf")
        with open("Axis_Pro_Statement.pdf", "rb") as f:
            st.download_button("Download Final Official PDF", f, file_name="Axis_Official_Statement.pdf")
