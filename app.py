import streamlit as st
from fpdf import FPDF

# 1. Login System
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 MFS Login")
    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "Mohit" and pw == "MFS5959":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Galat Password!")
    st.stop()

# 2. Generator UI
st.title("🏦 Mohit Financial Services")
st.subheader("Professional Statement Generator")

col1, col2 = st.columns(2)
with col1:
    bank = st.selectbox("Bank Name", ["STATE BANK OF INDIA", "AXIS BANK", "TATA MOTORS PAYROLL"])
    name = st.text_input("Customer Name", "Mohit Kumar Rai")
with col2:
    acc_no = st.text_input("Account Number", "XXXX XXXX 5959")
    opening_bal = st.number_input("Opening Balance", value=50000.0)

st.divider()
st.write("### Add Transactions")

if 'rows' not in st.session_state:
    st.session_state.rows = [{"date": "01-03-2026", "desc": "Salary - Tata Motors Ltd", "type": "Deposit", "amt": 80000.0}]

for i, row in enumerate(st.session_state.rows):
    c1, c2, c3, c4 = st.columns([2, 4, 2, 2])
    st.session_state.rows[i]["date"] = c1.text_input(f"Date", row["date"], key=f"d{i}")
    st.session_state.rows[i]["desc"] = c2.text_input(f"Description", row["desc"], key=f"p{i}")
    st.session_state.rows[i]["type"] = c3.selectbox(f"Type", ["Deposit", "Withdrawal"], index=0 if row["type"]=="Deposit" else 1, key=f"t{i}")
    st.session_state.rows[i]["amt"] = c4.number_input(f"Amount", value=row["amt"], key=f"a{i}")

if st.button("+ Add Row"):
    st.session_state.rows.append({"date": "02-03-2026", "desc": "UPI Transfer", "type": "Withdrawal", "amt": 0.0})

# 3. PDF Generation
if st.button("Generate Professional PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{bank} STATEMENT", 0, 1, 'C')
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, f"Account Holder: {name}", 0, 1)
    pdf.cell(0, 7, f"Account Number: {acc_no}", 0, 1)
    pdf.ln(5)
    
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(25, 10, "Date", 1, 0, 'C', True)
    pdf.cell(75, 10, "Particulars", 1, 0, 'C', True)
    pdf.cell(30, 10, "Withdrawal", 1, 0, 'C', True)
    pdf.cell(30, 10, "Deposit", 1, 0, 'C', True)
    pdf.cell(30, 10, "Balance", 1, 1, 'C', True)
    
    pdf.set_font("Arial", '', 9)
    current_bal = opening_bal
    for r in st.session_state.rows:
        w = r["amt"] if r["type"] == "Withdrawal" else 0.0
        d = r["amt"] if r["type"] == "Deposit" else 0.0
        current_bal = current_bal + d - w
        pdf.cell(25, 8, r["date"], 1)
        pdf.cell(75, 8, r["desc"][:40], 1)
        pdf.cell(30, 8, f"{w:,.2f}" if w > 0 else "0.00", 1, 0, 'R')
        pdf.cell(30, 8, f"{d:,.2f}" if d > 0 else "0.00", 1, 0, 'R')
        pdf.cell(30, 8, f"{current_bal:,.2f}", 1, 1, 'R')

    pdf.output("mfs_statement.pdf")
    with open("mfs_statement.pdf", "rb") as f:
        st.download_button("Download Professional Statement", f, "MFS_Statement.pdf")
        
