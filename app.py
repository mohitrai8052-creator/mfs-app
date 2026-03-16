import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Axis Statement System", layout="wide")

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

st.title("🏦 Axis Bank Professional Statement")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", "DNYANESHWAR RAMDAS BAVASKAR")
    address = st.text_area("Address", "GL G 3 MAHALAXMI APPARTMENT 2\nNARAYAN NAGAR SOCIETY\nPUNAGAM SURAT\nGUJARAT-395010")
    cust_id = st.text_input("Cust ID", "976307289")
with col2:
    acc_no = st.text_input("Acc No", "925010033967742")
    ifsc = st.text_input("IFSC", "UTIB0001306")
    micr = st.text_input("MICR", "395211007")
    opening_bal = st.number_input("Opening Balance", value=0.0)

salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")

if st.button("🚀 Taiyar Karein"):
    st.session_state.axis_data = generate_axis_data(opening_bal, salary_input)
    st.success("Data ready!")

if "axis_data" in st.session_state:
    if st.button("📥 Download Official Copy"):
        pdf = FPDF()
        pdf.add_page()
        
        # --- TOP HEADER ---
        pdf.set_font("Helvetica", 'B', 15)
        pdf.set_text_color(151, 27, 47)
        pdf.cell(0, 10, "AXIS BANK", 0, 1, 'L')
        
        # --- CUSTOMER DETAILS ---
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", '', 9)
        pdf.multi_cell(0, 4.5, f"{name}\nJoint Holder :--\n{address}\nRegistered Mobile No: XXXXXX5959")
        pdf.ln(4)

        # --- BANK INFO ---
        pdf.set_font("Helvetica", '', 8)
        pdf.cell(0, 4, f"Customer ID: {cust_id}  IFSC Code: {ifsc}  MICR Code : {micr}", 0, 1, 'L')
        pdf.cell(0, 4, "Nominee Registered: Y  Nominee Name: VANDANA", 0, 1, 'L')
        pdf.ln(2)
        pdf.set_font("Helvetica", 'B', 9)
        pdf.cell(0, 6, f"Statement of Axis Account No : {acc_no} for the period (01-09-2025 To 08-02-2026)", 0, 1, 'L')
        pdf.ln(2)

        # --- TABLE HEADER --- (Plain lines, No Boxes)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.set_font("Helvetica", 'B', 7)
        pdf.cell(20, 7, "Tran Date", 0, 0, 'C')
        pdf.cell(15, 7, "Chq No", 0, 0, 'C')
        pdf.cell(75, 7, "Particulars", 0, 0, 'C')
        pdf.cell(25, 7, "Debit", 0, 0, 'C')
        pdf.cell(25, 7, "Credit", 0, 0, 'C')
        pdf.cell(25, 7, "Balance", 0, 0, 'C')
        pdf.cell(10, 7, "Init.", 0, 1, 'C')
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())

        # --- OPENING BALANCE ---
        pdf.set_font("Helvetica", '', 7)
        pdf.cell(110, 6, "OPENING BALANCE", 0, 0, 'L')
        pdf.cell(25, 6, "", 0, 0)
        pdf.cell(25, 6, "", 0, 0)
        pdf.cell(25, 6, f"{opening_bal:,.2f}", 0, 1, 'R')

        # --- ROWS (No Border) ---
        for row in st.session_state.axis_data:
            pdf.cell(20, 5, row['date'], 0, 0, 'C')
            pdf.cell(15, 5, "", 0, 0)
            pdf.cell(75, 5, f" {row['desc']}", 0, 0, 'L')
            pdf.cell(25, 5, f"{row['wit']:,.2f} " if row['wit']>0 else "", 0, 0, 'R')
            pdf.cell(25, 5, f"{row['dep']:,.2f} " if row['dep']>0 else "", 0, 0, 'R')
            pdf.cell(25, 5, f"{row['bal']:,.2f} ", 0, 0, 'R')
            pdf.cell(10, 5, "101", 0, 1, 'C')

        # --- FOOTER ---
        pdf.ln(10)
        pdf.set_font("Helvetica", '', 6)
        footer = "REGISTERED OFFICE - AXIS BANK LTD, TRISHUL, Ahmedabad. 380006.\nThis is a system generated output and requires no signature.\n++++ End of Statement ++++"
        pdf.multi_cell(0, 4, footer, 0, 'C')
            
        pdf.output("Axis_Final_Statement.pdf")
        with open("Axis_Final_Statement.pdf", "rb") as f:
            st.download_button("Download Now", f, file_name="Axis_Official_Statement.pdf")
