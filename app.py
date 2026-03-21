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
    # Mar 2026 se piche ka data
    curr_date = datetime(2026, 3, 18)
    for i in range(1, 20):
        d_str = curr_date.strftime("%d %b %Y")
        ref = f"UPI-{random.randint(600000000000, 699999999999)}"
        wit = random.uniform(100, 1500)
        curr_bal -= wit
        data.append({"#": i, "date": d_str, "desc": "UPI/PURCHASE/ONLINE", "ref": ref, "wit": wit, "bal": curr_bal})
        curr_date -= timedelta(days=random.randint(1, 2))
    return data

st.title("🏦 Kotak Property-Lock Engine")

# 1. Original File Upload (Bank ki asli file yahan select karein)
uploaded_file = st.file_uploader("Upload Original Kotak PDF (for Metadata)", type="pdf")

if uploaded_file:
    st.success("Original Metadata Locked!")
    
    if st.button("🚀 Generate Data on Original Base"):
        transactions = get_kotak_data(201.87)
        
        # 2. Transparent Layer banayein data ke liye
        overlay_buf = io.BytesIO()
        c = canvas.Canvas(overlay_buf, pagesize=A4)
        c.setFont("Helvetica", 7.5)
        
        # Coordinates (Original Kotak layout ke hisaab se)
        y = 182*mm 
        for row in transactions:
            c.drawString(17*mm, y, str(row['#']))
            c.drawString(25*mm, y, row['date'])
            c.drawString(50*mm, y, row['desc'])
            c.drawString(110*mm, y, row['ref'])
            c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 6.1*mm 
            
        c.save()
        overlay_buf.seek(0)
        
        # 3. Merge Overlay with Original
        base_pdf = PdfReader(uploaded_file)
        overlay_pdf = PdfReader(overlay_buf)
        
        # Pehle page par merge karein
        PageMerge(base_pdf.pages[0]).add(overlay_pdf.pages[0]).render()
        
        # 4. Save Final PDF (Metadata base_pdf se copy hota hai)
        final_buf = io.BytesIO()
        writer = PdfWriter()
        writer.write(final_buf, base_pdf)
        
        st.download_button("📥 Download Final Statement", final_buf.getvalue(), "Kotak_Statement.pdf")
