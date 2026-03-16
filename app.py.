import streamlit as st
from fpdf import FPDF
from num2words import num2words
import datetime

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

# 2. Generator Logic
st.title("🏦 Mohit Financial Services")
bank = st.selectbox("Bank Layout", ["SBI", "Axis", "MFS"])
name = st.text_input("Customer Name", "Mohit Kumar Rai")
bal = st.number_input("Opening Balance", value=0.0)

# 3. PDF Function
if st.button("Generate & Download PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"{bank} STATEMENT", 1, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Name: {name}", 0, 1)
    pdf.cell(0, 10, f"Balance: {bal}", 0, 1)
    
    # Words conversion
    words = num2words(bal, lang='en_IN').title()
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"In Words: {words} Only")
    
    pdf.output("stmt.pdf")
    with open("stmt.pdf", "rb") as f:
        st.download_button("Download Now", f, file_name="Statement.pdf")
