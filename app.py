import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
from datetime import datetime, timedelta
import io

# --- 1. Kotak Style Data Generator (6 Months) ---
def get_kotak_data(opening_bal):
    transactions = []
    current_bal = opening_bal
    # April 2025 se Oct 2025 tak
    curr_date = datetime(2025, 10, 6, 11, 0)
    end_date = datetime(2025, 4, 7, 10, 0)
    
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d/%m/%Y")
        ref = f"{random.randint(1000000000, 9999999999)}"
        
        # Monthly Salary CR
        if curr_date.day in [5, 6, 7] and random.random() > 0.8:
            desc = "CMS-SALARY/TATA MOTORS LTD/"
            dep, wit = 80000.0, 0.0
        else:
            desc = f"UPI/DR/{ref}/PAYTM/PAYMENT"
            dep, wit = 0.0, random.uniform(100, 4500)
            
        current_bal = current_bal + dep - wit
        transactions.append({"d": d_str, "desc": desc, "ref": ref, "wit": wit, "dep": dep, "bal": current_bal})
        curr_date -= timedelta(hours=random.randint(15, 45))
    return transactions

st.set_page_config(page_title="Kotak Bank Statement", layout="wide")
st.title("🏦 Kotak Mahindra Bank Official Statement")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("Customer Name", "Mr. ASHISH TIWARI")
    acc_no = st.text_input("Account Number", "9876543210")
    crn = st.text_input("CRN Number", "123456789")
with col2:
    ifsc = st.text_input("IFSC Code", "KKBK0000123")
    branch = st.text_input("Branch Name", "ASHOK NAGAR, BHOPAL")
    op_bal = st.number_input("Opening Balance (7 Apr)", value=5000.00)

if st.button("🚀 Step 1: Generate Kotak Data"):
    st.session_state.kotak_data = get_kotak_data(op_bal)
    st.success(f"Generated {len(st.session_state.kotak_data)} transactions for 6 months!")

if "kotak_data" in st.session_state:
    if st.button("📥 Step 2: Download Kotak PDF"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        
        # Metadata
        c.setAuthor("Kotak Mahindra Bank")
        c.setTitle("Account Statement")

        def draw_kotak_header(can):
            can.setFont("Helvetica-Bold", 14)
            can.drawString(20*mm, 280*mm, "KOTAK MAHINDRA BANK")
            
            can.setFont("Helvetica", 9)
            can.drawString(20*mm, 270*mm, f"Name: {name}")
            can.drawString(20*mm, 265*mm, f"Account No: {acc_no}")
            can.drawString(20*mm, 260*mm, f"CRN: {crn}")
            
            can.drawString(140*mm, 270*mm, f"IFSC: {ifsc}")
            can.drawString(140*mm, 265*mm, f"Branch: {branch}")
            
            # Statement Duration
            can.setFont("Helvetica-Bold", 10)
            can.drawString(20*mm, 245*mm, "Statement Period: 07/04/2025 to 06/10/2025")
            
            # Table Header
            y_h = 235*mm
            can.setLineWidth(0.5)
            can.line(18*mm, y_h+2*mm, 195*mm, y_h+2*mm)
            can.setFont("Helvetica-Bold", 8)
            can.drawString(20*mm, y_h, "Date")
            can.drawString(45*mm, y_h, "Narration / Description")
            can.drawRightString(130*mm, y_h, "Withdrawal (Dr)")
            can.drawRightString(160*mm, y_h, "Deposit (Cr)")
            can.drawRightString(192*mm, y_h, "Balance")
            can.line(18*mm, y_h-2*mm, 195*mm, y_h-2*mm)
            return y_h - 7*mm

        y = draw_kotak_header(c)
        c.setFont("Helvetica", 7.5)
        
        for row in st.session_state.kotak_data:
            c.drawString(20*mm, y, row['d'])
            c.drawString(45*mm, y, row['desc'][:50])
            if row['wit'] > 0: c.drawRightString(130*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(160*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 5*mm
            
            if y < 20*mm:
                c.showPage()
                y = draw_kotak_header(c)
                c.setFont("Helvetica", 7.5)
        
        c.save()
        st.download_button("Download Kotak Statement", buf.getvalue(), "Kotak_Statement.pdf")
