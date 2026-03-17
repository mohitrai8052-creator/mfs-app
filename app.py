limport streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import random
from datetime import datetime, timedelta
import io

# --- 6 Month Duration Data Generator ---
def generate_sbi_6month_data(op_bal, sal_text):
    data = []
    curr_bal = op_bal
    # Start Date: 7 April 2025, End Date: 6 Oct 2025
    current_date = datetime(2025, 10, 6, 11, 0)
    end_date = datetime(2025, 4, 7, 10, 0)
    
    while current_date >= end_date:
        d_str = current_date.strftime("%d %b %Y")
        
        # Salary Entry (Har mahine ki 5-7 tarikh ke beech)
        if current_date.day in [5, 6, 7] and random.random() > 0.7:
            desc, dep, wit = sal_text, 80000.0, 0.0
        else:
            # Regular Transactions
            ref = str(random.randint(100000000000, 999999999999))
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(50, 5000)
            
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "wit": wit, "dep": dep, "bal": curr_bal})
        
        # Gap between transactions (12 to 48 hours)
        current_date -= timedelta(hours=random.randint(12, 48))
        
    return data

st.set_page_config(page_title="SBI 6-Month Statement", layout="wide")
st.title("🏦 SBI 6-Month Professional System")

c1, c2 = st.columns(2)
with c1:
    name = st.text_input("Name", "Mr. ASHISH TIWARI")
    addr = st.text_area("Address", "H NO 16 DWARKA NAGAR\nGALI NO 06 COACH FACTORY\nBHOPAL-462010")
    acc = st.text_input("Account Number", "00000031144336469")
with c2:
    branch = st.text_input("Branch", "STATION ROAD, ASHOKNAGAR")
    ifsc = st.text_input("IFSC", "SBIN0030082")
    cif = st.text_input("CIF", "85774527603")
    op_bal = st.number_input("Opening Balance (as on 7 Apr)", value=42.37)

if st.button("🚀 Generate 6-Month Statement"):
    st.session_state.duration_data = generate_sbi_6month_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success(f"Generated {len(st.session_state.duration_data)} transactions for 6 months!")

if "duration_data" in st.session_state:
    if st.button("📥 Download Official 6-Month PDF"):
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=A4)
        
        # --- PDF Drawing Logic (Multi-page) ---
        def draw_header(canvas_obj, pagenum):
            canvas_obj.setFont("Helvetica-Bold", 18)
            canvas_obj.drawString(20*mm, 282*mm, "SBI")
            canvas_obj.setFont("Helvetica", 8)
            # Left Header
            canvas_obj.drawString(20*mm, 270*mm, f"Account Name : {name}")
            canvas_obj.drawString(20*mm, 265*mm, f"Address : {addr.splitlines()[0]}")
            canvas_obj.drawString(20*mm, 245*mm, f"Date : 6 Oct 2025")
            # Right Header
            canvas_obj.drawString(115*mm, 270*mm, f"Account Number : {acc}")
            canvas_obj.drawString(115*mm, 265*mm, f"Branch : {branch}")
            canvas_obj.drawString(115*mm, 255*mm, f"IFS Code : {ifsc}")
            
            canvas_obj.setFont("Helvetica-Bold", 9)
            canvas_obj.drawString(20*mm, 230*mm, "Account Statement from 7 Apr 2025 to 6 Oct 2025")
            
            # Table Header
            y_h = 220*mm
            canvas_obj.setLineWidth(0.1)
            canvas_obj.line(18*mm, y_h+4*mm, 195*mm, y_h+4*mm)
            canvas_obj.setFont("Helvetica-Bold", 7.5)
            canvas_obj.drawString(20*mm, y_h, "Txn Date")
            canvas_obj.drawString(45*mm, y_h, "Value Date")
            canvas_obj.drawString(70*mm, y_h, "Description")
            canvas_obj.drawRightString(145*mm, y_h, "Debit")
            canvas_obj.drawRightString(168*mm, y_h, "Credit")
            canvas_obj.drawRightString(192*mm, y_h, "Balance")
            canvas_obj.line(18*mm, y_h-2*mm, 195*mm, y_h-2*mm)
            return y_h - 7*mm

        y = draw_header(c, 1)
        c.setFont("Helvetica", 6.8)
        
        for i, row in enumerate(st.session_state.duration_data):
            c.drawString(20*mm, y, row['d'])
            c.drawString(45*mm, y, row['d'])
            c.drawString(70*mm, y, row['desc'][:55])
            if row['wit'] > 0: c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0: c.drawRightString(168*mm, y, f"{row['dep']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 4.8*mm
            
            # New Page Logic
            if y < 20*mm:
                c.showPage()
                y = draw_header(c, 2)
                c.setFont("Helvetica", 6.8)
        
        c.save()
        st.download_button("📥 Download 6-Month Statement", buf.getvalue(), "SBI_6Month_Statement.pdf")
