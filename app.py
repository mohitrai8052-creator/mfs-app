from fpdf import FPDF

class SBIStatement(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'State Bank of India - Account Statement', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

# Initialize PDF
pdf = SBIStatement()
pdf.add_page()
pdf.set_font('Arial', '', 10)
pdf.cell(0, 10, 'Account Number: XXXXXXXX1234', 0, 1)
pdf.cell(0, 10, 'Period: 01-Jan-2025 to 30-Jan-2025', 0, 1)
# ... add transaction table logic here ...
pdf.output('SBI_Statement.pdf')
