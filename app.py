import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
from datetime import datetime, timedelta
import io

def generate_sbi_data(op_bal, sal_text):
    data = []
    curr_bal = op_bal
    current_date = datetime(2025, 10, 6, 10, 30)
    end_date = datetime(2025, 4, 7, 10, 0)
    
    while current_date >= end_date:
        d_str = current_date.strftime("%d %b %Y")
        if current_date.day in [5, 6, 7] and random.random() > 0.8:
            desc, dep, wit = sal_text, 80000.0, 0.0
        else:
            ref = str(random.randint(100000000000, 999999999999))
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(50, 4500)
            
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "wit": wit, "dep": dep, "bal": curr_bal})
        current_date -= timedelta(hours=random.randint(12, 40))
    return data

st.title("🏦 SBI Official Format Engine")

# User Inputs
c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Account Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Account Number", "00000031144336469")
with c2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFS Code", "SBIN0030082")
    cif = st.text_input("CIF No.", "85774527603")
    op_bal = st.number_input("Opening Balance (7 Apr)", value=42.37)

if st.button("🚀 Process Original Layout"):
    st.session_state.final_bank_data = generate_sbi_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success("Layout Finalized with Metadata!")

if "final_bank_data" in st.session_state:
    if st.button("📥 Download Final Statement"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        
        # --- SETTING SYSTEM METADATA (Very Important for Originality) ---
        c.setAuthor("State Bank of India")
        c.setCreator("iText 2.1.7 by 1T3XT")
        c.setProducer("iText 2.1.7 by 1T3XT")
        c.setSubject("Account Statement")
        c.setTitle("Statement_6Month")

        def draw_template(can):
            can.setFont("Helvetica-Bold", 16)
            can.drawString(20*mm, 282*mm, "SBI")
            can.setFont("Courier", 8.5)
            # Alignment check
            can.drawString(20*mm, 272*mm, f"Account Name         : {name}")
            can.drawString(115*mm, 272*mm, f"Account Number : {acc}")
            can.drawString(20*mm, 267*mm, f"Address              : {addr.splitlines()[0]}")
            can.drawString(115*mm, 267*mm, f"Branch         : {branch}")
            can.drawString(20*mm, 245*mm, f"Date                 : 6 Oct 2025")
            can.drawString(115*mm, 255*mm, f"IFS Code       : {ifsc}")
            can.setFont("Courier-Bold", 9)
            can.drawString(20*mm, 232*mm, "Account Statement from 7 Apr 2025 to 6 Oct 2025")
            # Table Lines
            can.setLineWidth(0.1)
            can.line(18*mm, 226*mm, 195*mm, 226*mm)
            can.setFont("Courier-Bold", 7.5)
            can.drawString(20*mm, 222*mm, "Txn Date")
            can.drawString(42*mm, 222*mm, "Value Date")
            can.drawString(68*mm, 222*mm, "Description")
            can.drawRightString(148*mm, 222*mm, "Debit")
            can.drawRightString(170*mm, 222*mm, "Credit")
            can.drawRightString(192*mm, 222*mm, "Balance")
            can.line(18*mm, 219*mm, 195*mm, 219*mm)
            return 214*mm

        y = draw_template(c)
        c.setFont("Courier", 7)
        for row in st.session_state.final_bank_data:
            c.drawString(20*mm, y, row['d'])
            c.drawString(42*mm, y, row['d'])
            c.drawString(68*mm, y, row['desc'][:58])
            if row['wit'] > 0: c.drawRightString(148*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(170*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 4.2*mm
            if y < 20*mm:
                c.showPage()
                y = draw_template(c)
                c.setFont("Courier", 7)
        
        c.save()
        st.download_button("Download Final Original Copy", buf.getvalue(), "SBI_Official_6Month.pdf")
