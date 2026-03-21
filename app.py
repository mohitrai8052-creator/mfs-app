import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pdfrw import PdfReader, PdfWriter, PageMerge
import io
import random
from datetime import datetime, timedelta

# --- 1. Authentic Data Generator ---
def get_kotak_data(op_bal):
    data = []
    curr_bal = op_bal
    # Mar 2026 se piche 1 month ka testing data
    curr_date = datetime(2026, 3, 18)
    for i in range(1, 25):
        d_str = curr_date.strftime("%d %b %Y")
        ref = f"UPI-{random.randint(600000000000, 699999999999)}"
        wit = random.uniform(100, 2000)
        curr_bal -= wit
        data.append({"#": i, "date": d_str, "desc": "UPI/PURCHASE/MERCHANT", "ref": ref, "wit": wit, "bal": curr_bal})
        curr_date -= timedelta(days=random.randint(1, 2))
    return data

st.title("🏦 Kotak Original Template Fixer")

# 1. Original File Upload (Pehle bank ki asli file yahan upload karein)
uploaded_file = st.file_uploader("Upload Original Kotak PDF (Properties copy karne ke liye)", type="pdf")

if uploaded_file:
    st.success("Original PDF Loaded! Properties locked.")
    
    if st.button("🚀 Generate Statement on Original Template"):
        # Data taiyar karein
        transactions = get_kotak_data(201.87)
        
        # 2. Ek Transparent Layer (Overlay) banayein data ke liye
        overlay_buf = io.BytesIO()
        c = canvas.Canvas(overlay_buf, pagesize=A4)
        c.setFont("Helvetica", 7.5)
        
        # Original layout ke hisaab se coordinates (yahan data print hoga)
        y = 182*mm 
        for row in transactions:
            c.drawString(17*mm, y, str(row['#']))
            c.drawString(25*mm, y, row['date'])
            c.drawString(50*mm, y, row['desc'])
            c.drawString(110*mm, y, row['ref'])
            c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 6.1*mm # Row spacing
            
        c.save()
        overlay_buf.seek(0)
        
        # 3. Dono ko merge karein
        base_pdf = PdfReader(uploaded_file)
        overlay_pdf = PdfReader(overlay_buf)
        
        # Pehle page par data merge karein
        PageMerge(base_pdf.pages[0]).add(overlay_pdf.pages[0]).render()
        
        # 4. Final Save (Isse properties base_pdf ki hi rehti hain)
        final_buf = io.BytesIO()
        writer = PdfWriter()
        writer.write(final_buf, base_pdf)
        
        st.download_button("📥 Download Final Statement", final_buf.getvalue(), "Kotak_Statement_Final.pdf")
