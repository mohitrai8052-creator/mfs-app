import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from pdfrw import PdfReader, PdfWriter, PageMerge
import io
import random
from datetime import datetime, timedelta

# --- 1. Authentic Kotak Data Generator (With Tata Motors Salary) ---
def get_kotak_salary_data(op_bal):
    data = []
    curr_bal = op_bal
    # 1 Feb 2026 se 18 Mar 2026 tak ka loop (Aapki file ke dates)
    curr_date = datetime(2026, 3, 18)
    end_date = datetime(2026, 2, 1)
    
    count = 1
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        ref = f"UPI-{random.randint(600000000000, 699999999999)}"
        
        # Salary Entry (Har mahine ki 1st ya 2nd date ko)
        if curr_date.day in [1, 2]:
            desc = "CMS-SALARY/TATA MOTORS LTD/FEB26"
            dep, wit = 85000.0, 0.0
        else:
            # Random UPI spends
            desc = f"UPI/PAYMENT TO MERCHANT/{random.randint(100, 999)}/Purchase"
            dep, wit = 0.0, random.uniform(50, 2500)
            
        curr_bal = curr_bal + dep - wit
        data.append({
            "#": count, 
            "date": d_str, 
            "desc": desc, 
            "ref": ref, 
            "wit": wit, 
            "dep": dep, 
            "bal": curr_bal
        })
        curr_date -= timedelta(hours=random.randint(18, 48))
        count += 1
    return data[::-1] # Seedha (Chronological) order mein karne ke liye

st.title("🏦 Kotak Mahindra - Property Lock Engine")

# 1. Original File Upload
uploaded_file = st.file_uploader("Upload Original Kotak PDF (Metadata ke liye)", type="pdf")

if uploaded_file:
    st.success("Original OpenPDF Metadata Locked!")
    
    if st.button("🚀 Generate Salary Statement"):
        transactions = get_kotak_salary_data(201.87)
        
        # 2. Transparent Layer banayein data ke liye
        overlay_buf = io.BytesIO()
        c = canvas.Canvas(overlay_buf, pagesize=A4)
        c.setFont("Helvetica", 7) # Kotak standard font size
        
        # Original layout ke coordinates jahan 'Opening Balance' ke baad entries shuru hoti hain
        y = 175*mm 
        for row in transactions:
            # Columns alignment as per Kotak format
            c.drawString(17*mm, y, str(row['#']))
            c.drawString(25*mm, y, row['date'])
            c.drawString(48*mm, y, row['desc'][:40]) # Description
            c.drawString(108*mm, y, row['ref']) # Ref No.
            
            if row['wit'] > 0:
                c.drawRightString(145*mm, y, f"{row['wit']:,.2f}")
            if row['dep'] > 0:
                c.drawRightString(170*mm, y, f"{row['dep']:,.2f}")
                
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 6.1*mm # Row height adjustment
            
            if y < 30*mm: # Page break logic agar entries zyada hain
                c.showPage()
                y = 250*mm
                c.setFont("Helvetica", 7)
            
        c.save()
        overlay_buf.seek(0)
        
        # 3. Merge Overlay with Original
        base_pdf = PdfReader(uploaded_file)
        overlay_pdf = PdfReader(overlay_buf)
        
        # Pehle page par data chhapna
        PageMerge(base_pdf.pages[0]).add(overlay_pdf.pages[0]).render()
        
        # 4. Save Final PDF (Properties are preserved)
        final_buf = io.BytesIO()
        writer = PdfWriter()
        writer.write(final_buf, base_pdf)
        
        st.download_button("📥 Download Final Kotak Statement", final_buf.getvalue(), "Kotak_Statement_Final.pdf")
