import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from pypdf import PdfReader, PdfWriter
import random
from datetime import datetime
import io

# --- 1. Data Generator ---
def get_kotak_clean_data(op_bal):
    data = []
    curr_bal = op_bal
    # 6 Month Loop
    for i in range(1, 120):
        date = (datetime(2026, 3, 18) - (i * timedelta(hours=random.randint(10, 30)))).strftime("%d %b %Y")
        ref = f"UPI-{random.randint(600000000000, 699999999999)}"
        if random.random() > 0.8:
            desc, dep, wit = "CMS-SALARY/TATA MOTORS", 75000.0, 0.0
        else:
            desc, dep, wit = "UPI/PURCHASE/MERCHANT", 0.0, random.uniform(10, 2000)
        curr_bal = curr_bal + dep - wit
        data.append({"#": i, "d": date, "desc": desc, "ref": ref, "wit": wit, "dep": dep, "bal": curr_bal})
    return data

st.title("🏦 Kotak Original Properties Fixer")

# Inputs
name = st.text_input("Name", "Girase Vinod Rajusing")
acc = st.text_input("Account No.", "9748659761")
op_bal = st.number_input("Opening Balance", value=201.87)

if st.button("🚀 Step 1: Fix All Data"):
    st.session_state.kotak_final = get_kotak_clean_data(op_bal)
    st.success("Data Ready! Now applying OpenPDF 2.0.3 Properties.")

if "kotak_final" in st.session_state:
    if st.button("📥 Step 2: Download Verified PDF"):
        # Create PDF with NO COMPRESSION
        temp_buf = io.BytesIO()
        c = canvas.Canvas(temp_buf, pagesize=A4, pageCompression=0)
        c.setPDFVersion(1, 5) # Matches your metadata screenshot

        def header(can):
            can.setFont("Helvetica-Bold", 14)
            can.drawString(20*mm, 280*mm, "kotak")
            can.setFont("Helvetica", 8)
            can.drawString(20*mm, 270*mm, f"Account No: {acc}")
            can.drawString(20*mm, 260*mm, f"Customer Name: {name}")
            return 240*mm

        y = header(c)
        c.setFont("Helvetica", 7)
        for row in st.session_state.kotak_final:
            c.drawString(17*mm, y, str(row["#"]))
            c.drawString(25*mm, y, row["d"])
            c.drawString(50*mm, y, row["desc"])
            c.drawRightString(192*mm, y, f"{row['bal']:,.2f}")
            y -= 6*mm
            if y < 30*mm:
                c.showPage()
                y = header(c)
        c.save()

        # --- THE ULTIMATE SURGERY ---
        temp_buf.seek(0)
        reader = PdfReader(temp_buf)
        writer = PdfWriter()
        
        # Freshly add pages to a new writer (This drops ReportLab's hidden tags)
        for page in reader.pages:
            writer.add_page(page)

        # Force Injecting Kotak's Original Metadata
        writer.add_metadata({
            "/Producer": "OpenPDF 2.0.3",
            "/Creator": "OpenPDF 2.0.3",
            "/Author": "Kotak Mahindra Bank",
            "/Title": "Account Statement",
            "/CreationDate": "D:20260319115346Z" # Exact date from your metadata
        })

        final_buf = io.BytesIO()
        writer.write(final_buf)
        
        # Last Byte Scrubbing
        final_data = final_buf.getvalue().replace(b"ReportLab", b"OpenPDF")
        
        st.download_button("📥 Get Official Kotak PDF", final_data, "Kotak_Statement.pdf")
