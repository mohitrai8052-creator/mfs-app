import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
from datetime import datetime, timedelta
import io

def generate_sbi_data(opening_bal, salary_text):
    data = []
    curr_bal = opening_bal
    start_date = datetime(2025, 10, 6)
    # 150 entries for 6 months
    for i in range(150):
        d = start_date - timedelta(hours=i*30)
        d_str = d.strftime("%d %b %Y")
        if d.day in [5,6,7] and i % 25 == 0:
            desc, dep, wit = salary_text, 80000.0, 0.0
        else:
            ref = f"{random.randint(100000000000, 999999999999)}"
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(50, 3500)
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "wit": wit, "dep": dep, "bal": curr_bal})
    return data

st.title("🏦 SBI Original Format Generator")

# Inputs
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Account Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Account Number", "00000031144336469")
with c2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFS Code", "SBIN0030082")
    cif = st.text_input("CIF No.", "85774527603")
    op_bal = st.number_input("Opening Balance", value=42.37)

if st.button("🚀 Step 1: Fix Formatting"):
    st.session_state.final_data = generate_sbi_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success("Format Fixed!")

if "final_data" in st.session_state:
    if st.button("📥 Step 2: Download Original PDF"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        
        # --- Drawing Top Header ---
        c.setFont("Helvetica-Bold", 18)
        c.drawString(20*mm, 280*mm, "SBI")
        
        c.setFont("Helvetica", 8)
        # Left Details
        c.drawString(20*mm, 268*mm, f"Account Name  : {name}")
        c.drawString(20*mm, 263*mm, f"Address       : {addr.splitlines()[0]}")
        if len(addr.splitlines()) > 1:
            c.drawString(42*mm, 259*mm, addr.splitlines()[1])
        c.drawString(20*mm, 245*mm, "Date          : 6 Oct 2025")
        c.drawString(20*mm, 240*mm, "Account Description : SBCHQ-RSP-PUBIND")
        
        # Right Details
        c.drawString(115*mm, 268*mm, f"Account Number : {acc}")
        c.drawString(115*mm, 263*mm, f"Branch         : {branch}")
        c.drawString(115*mm, 258*mm, f"CIF No.        : {cif}")
        c.drawString(115*mm, 253*mm, f"IFS Code       : {ifsc}")
        
        c.setFont("Helvetica-Bold", 9)
        c.drawString(20*mm, 225*mm, "Account Statement from 7 Apr 2025 to 6 Oct 2025")
        
        # --- Table Lines and Headers ---
        y = 215*mm
        c.setLineWidth(0.2)
        c.line(18*mm, y+5*mm, 195*mm, y+5*mm) # Top Border
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(20*mm, y, "Txn Date")
        c.drawString(45*mm, y, "Value Date")
        c.drawString(70*mm, y, "Description")
        c.drawRightString(145*mm, y, "Debit")
        c.drawRightString(168*mm, y, "Credit")
        c.drawRightString(192*mm, y, "Balance")
        c.line(18*mm, y-2*mm, 195*mm, y-2*mm) # Header Bottom
        
        # --- Data Rows ---
        y -= 7*mm
        c.setFont("Helvetica", 6.8)
        for row in st.session_state.final_data[:35]: # Page 1
            c.drawString(20*mm, y, row['d'])
            c.drawString(45*mm, y, row['d'])
            c.drawString(70*mm, y, row['desc'][:55])
            if row['wit'] > 0: c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(168*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 4.5*mm
            if y < 20*mm: break
        
        c.showPage()
        c.save()
        st.download_button("Download Final Original", buf.getvalue(), "SBI_Original_Copy.pdf")
