import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pdfrw import PdfReader, PdfWriter, PageMerge
import io
import random
from datetime import datetime, timedelta

# --- 1. Data Generator ---
def get_kotak_data(op_bal):
    data = []
    curr_bal = op_bal
    for i in range(1, 30): # Testing with 30 rows first
        date = (datetime(2026, 3, 18) - timedelta(days=i)).strftime("%d %b %Y")
        desc = "UPI/PURCHASE/MERCHANT/PAYMENT"
        wit = random.uniform(100, 2000)
        curr_bal -= wit
        data.append({"date": date, "desc": desc, "wit": wit, "bal": curr_bal})
    return data

st.title("🏦 Kotak Original Template Engine")

# Original File Upload
uploaded_file = st.file_uploader("Upload Original Kotak PDF (for Properties)", type="pdf")

if uploaded_file and st.button("🚀 Generate Overlaid PDF"):
    # 1. Generate Transactions
    transactions = get_kotak_data(201.87)
    
    # 2. Create an "Overlay" PDF (Transparent)
    overlay_buf = io.BytesIO()
    c = canvas.Canvas(overlay_buf, pagesize=A4)
    c.setFont("Helvetica", 7.5)
    
    y = 185*mm # Starting Y position on original Kotak page
    for row in transactions:
        c.drawString(25*mm, y, row['date'])
        c.drawString(50*mm, y, row['desc'])
        c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
        c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
        y -= 6*mm
    c.save()
    
    # 3. Merge Overlay with Original
    overlay_buf.seek(0)
    base_pdf = PdfReader(uploaded_file)
    overlay_pdf = PdfReader(overlay_buf)
    
    # Merge first page
    PageMerge(base_pdf.pages[0]).add(overlay_pdf.pages[0]).render()
    
    # 4. Save Final PDF (Properties are preserved from base_pdf)
    final_buf = io.BytesIO()
    writer = PdfWriter()
    writer.write(final_buf, base_pdf)
    
    st.download_button("📥 Download Property-Locked PDF", final_buf.getvalue(), "Kotak_Final.pdf")
