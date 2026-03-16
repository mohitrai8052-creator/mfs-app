import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="Axis Bank Official Copy", layout="wide")

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

st.title("🏦 Axis Bank Carbon Copy System")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Name", "DNYANESHWAR RAMDAS BAVASKAR")
    address = st.text_area("Full Address", "GL G 3 MAHALAXMI APPARTMENT 2\nNARAYAN NAGAR SOCIETY\nPUNAGAM PARVATPARVAT PATIYA\nSURAT\nGUJARAT-INDIA\n395010")
    cust_id = st.text_input("Customer ID", "976307289")
with col2:
    acc_no = st.text_input("Account No", "925010033967742")
    ifsc = st.text_input("IFSC", "UTIB0001306")
    micr = st.text_input("MICR", "395211007")
    opening_bal = st.number_input("Opening Balance", value=0.0)

salary_input = st.text_input("Salary Narration", "SALARY/TATA MOTORS LTD/MAR-26")

if st.button("🚀 Step 1: Generate Data"):
    st.session_state.axis_data = generate_axis_data(opening_bal, salary_input)
    st.success("Data ready!")

if "axis_data" in st.session_state:
    if st.button("📥 Step 2: Download Carbon Copy PDF"):
        pdf = FPDF()
        pdf.add_page()
        
        # --- CUSTOMER ADDRESS BLOCK ---
        pdf.set_font("Helvetica", '', 9)
        pdf.multi_cell(0, 5, f"{name}\nJoint Holder :--\n{address}\nRegistered Mobile No: XXXXXX2348\nRegistered Email ID: baXXXX98@gmail.com\nScheme:SB-EASY ACCESS SA (RUSU)")
        
        # --- AXIS BANK CENTER LOGO ---
        pdf.ln(5)
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(0, 10, "AXIS BANK", 0, 1, 'C')
        
        # --- ACCOUNT INFO BLOCK ---
        pdf.set_font("Helvetica", '', 8)
        info_text = f"Customer ID:{cust_id}  IFSC Code: {ifsc}  MICR Code : {micr}\nNominee Registered: Y  Nominee Name: VANDANA\nPAN:DLGPB1425Q  CKYC NUMBER:XXXXXXXXXX3370"
        pdf.multi_cell(0, 4, info_text, 0, 'C')
        pdf.ln(2)
        pdf.set_font("Helvetica", 'B', 9)
        pdf.cell(0, 6, f"Statement of Axis Account No : {acc_no} for the period (From: 01-09-2025 To: 08-02-2026)", 0, 1, 'L')
        pdf.ln(2)
        
        # --- TABLE HEADER ---
        pdf.set_font("Helvetica", 'B', 7)
        pdf.cell(20, 7, "Tran Date", "TB", 0, 'C')
        pdf.cell(15, 7, "Chq No", "TB", 0, 'C')
        pdf.cell(75, 7, "Particulars", "TB", 0, 'C')
        pdf.cell(25, 7, "Debit", "TB", 0, 'C')
        pdf.cell(25, 7, "Credit", "TB", 0, 'C')
        pdf.cell(25, 7, "Balance", "TB", 0, 'C')
        pdf.cell(10, 7, "Init. Br", "TB", 1, 'C')
        
        # --- ROWS ---
        pdf.set_font("Helvetica", '', 7)
        pdf.cell(20, 6, "", 0, 0)
        pdf.cell(15, 6, "", 0, 0)
        pdf.cell(75, 6, "OPENING BALANCE", 0, 0, 'L')
        pdf.cell(25, 6, "", 0, 0)
        pdf.cell(25, 6, "", 0, 0)
        pdf.cell(25, 6, f"{opening_bal:,.2f}", 0, 1, 'R')

        for row in st.session_state.axis_data:
            pdf.cell(20, 6, row['date'], 0, 0, 'C')
            pdf.cell(15, 6, "", 0, 0)
            pdf.cell(75, 6, f"{row['desc']}", 0, 0, 'L')
            pdf.cell(25, 6, f"{row['wit']:,.2f}" if row['wit']>0 else "", 0, 0, 'R')
            pdf.cell(25, 6, f"{row['dep']:,.2f}" if row['dep']>0 else "", 0, 0, 'R')
            pdf.cell(25, 6, f"{row['bal']:,.2f}", 0, 0, 'R')
            pdf.cell(10, 6, "101", 0, 1, 'C')
            
        # --- LEGENDS SECTION ---
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 8)
        pdf.cell(0, 10, "Legends:", 0, 1, 'L')
        pdf.set_font("Helvetica", '', 7)
        legends = "ICONN: Internet Banking | VMT-ICON: Visa Money Transfer | AUTOSWEEP: Transfer to FD\nCWDR: ATM Cash Withdrawal | PUR: POS Purchase | CLG: Cheque Clearing\nThis is a system generated output and requires no signature."
        pdf.multi_cell(0, 4, legends)
        pdf.ln(5)
        pdf.set_font("Helvetica", 'B', 8)
        pdf.cell(0, 5, "++++ End of Statement ++++", 0, 1, 'C')
            
        pdf.output("Axis_Carbon_Copy.pdf")
        with open("Axis_Carbon_Copy.pdf", "rb") as f:
            st.download_button("Download Original Copy", f, file_name="Axis_Official_Statement.pdf")
            
