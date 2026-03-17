import streamlit as st
from fpdf import FPDF
import random
from datetime import datetime, timedelta
import io

# Custom PDF Class to handle Metadata
class SBI_PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'SBI', 0, 1, 'L')
        self.ln(5)

def generate_sbi_data(op_bal, sal_text):
    data = []
    curr_bal = op_bal
    curr_date = datetime(2025, 10, 6, 10, 0)
    end_date = datetime(2025, 4, 7, 9, 0)
    while curr_date >= end_date:
        d_str = curr_date.strftime("%d %b %Y")
        if curr_date.day in [5, 6, 7] and random.random() > 0.8:
            desc, dep, wit = sal_text, 80000.0, 0.0
        else:
            ref = str(random.randint(100000000000, 999999999999))
            desc, dep, wit = f"TRANSFER-UPI/DR/{ref}/PAYTM", 0.0, random.uniform(100, 5000)
        curr_bal = curr_bal + dep - wit
        data.append({"d": d_str, "desc": desc, "wit": wit, "dep": dep, "bal": curr_bal})
        curr_date -= timedelta(hours=random.randint(15, 45))
    return data

st.title("🏦 SBI Final Master (fpdf version)")

# Inputs
name = st.text_input("Name", "Mr. ASHISH TIWARI")
acc = st.text_input("Acc No.", "00000031144336469")
op_bal = st.number_input("Opening Bal (7 Apr)", value=42.37)

if st.button("🚀 Step 1: Fix Data"):
    st.session_state.master_data = generate_sbi_data(op_bal, "BY TRANSFER-UPI/CR/TATA MOTORS LTD/SALARY")
    st.success("Data ready for fpdf engine!")

if "master_data" in st.session_state:
    if st.button("📥 Step 2: Download v1.4 Original PDF"):
        pdf = SBI_PDF()
        
        # --- THE FIX: Set Metadata BEFORE adding page ---
        pdf.set_author("State Bank of India")
        pdf.set_creator("iText 2.1.7 by 1T3XT")
        pdf.set_title("Statement_Account")
        # Producer is set via a hack in the final output string
        
        pdf.add_page()
        pdf.set_font("Courier", size=8)
        
        # Header Info
        pdf.cell(0, 5, f"Account Name   : {name}", 0, 1)
        pdf.cell(0, 5, f"Account Number : {acc}", 0, 1)
        pdf.ln(10)
        
        # Table Header
        pdf.set_font("Courier", 'B', 8)
        pdf.cell(30, 8, "Txn Date", 1)
        pdf.cell(80, 8, "Description", 1)
        pdf.cell(25, 8, "Debit", 1)
        pdf.cell(25, 8, "Credit", 1)
        pdf.cell(30, 8, "Balance", 1)
        pdf.ln()
        
        # Data Rows
        pdf.set_font("Courier", size=7)
        for row in st.session_state.master_data:
            pdf.cell(30, 6, row['d'], 1)
            pdf.cell(80, 6, row['desc'][:45], 1)
            pdf.cell(25, 6, f"{row['wit']:.2f}" if row['wit'] > 0 else "", 1)
            pdf.cell(25, 6, f"{row['dep']:.2f}" if row['dep'] > 0 else "", 1)
            pdf.cell(30, 6, f"{row['bal']:.2f}", 1)
            pdf.ln()
            
        # Get PDF String
        pdf_output = pdf.output(dest='S')
        
        # Binary Hack for Producer (fpdf doesn't have a direct method)
        if isinstance(pdf_output, str):
            pdf_bytes = pdf_output.encode('latin1')
        else:
            pdf_bytes = pdf_output
            
        # Manually Inject Producer into the PDF structure
        if b"/Producer" in pdf_bytes:
            # Replace default producer
            final_pdf = pdf_bytes.replace(b"/Producer (FPDF 1.7)", b"/Producer (iText 2.1.7 by 1T3XT)")
        else:
            # Add it if missing
            final_pdf = pdf_bytes.replace(b"/Author", b"/Producer (iText 2.1.7 by 1T3XT) /Author")

        st.download_button("📥 Click for Verified PDF", final_pdf, "SBI_Statement.pdf")
        })

        final_buf = io.BytesIO()
        writer.write(final_buf)
        
        # Binary Clean (Final Step)
        raw_data = final_buf.getvalue()
        raw_data = raw_data.replace(b"ReportLab", b"iText")
        
        st.download_button("📥 Get Original Properties PDF", raw_data, "SBI_Statement.pdf")
