from fpdf import FPDF
from datetime import datetime

class BankStatement(FPDF):
    def header(self):
        # Company Name & Logo area
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'MOHIT FINANCIAL SERVICES', ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Contact: 7047205959, 9109695959', ln=True, align='C')
        self.ln(10)

    def statement_details(self, name, acc_no):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Account Holder: {name}', ln=True)
        self.cell(0, 10, f'Account Number: {acc_no}', ln=True)
        self.cell(0, 10, f'Statement Date: {datetime.now().strftime("%d-%m-%Y")}', ln=True)
        self.ln(5)

    def draw_table(self, data):
        # Table Header
        self.set_fill_color(200, 220, 255)
        self.set_font('Arial', 'B', 10)
        self.cell(30, 10, 'Date', 1, 0, 'C', True)
        self.cell(80, 10, 'Description', 1, 0, 'C', True)
        self.cell(40, 10, 'Amount', 1, 0, 'C', True)
        self.cell(40, 10, 'Balance', 1, 1, 'C', True)

        # Table Rows
        self.set_font('Arial', '', 10)
        for row in data:
            self.cell(30, 10, row[0], 1)
            self.cell(80, 10, row[1], 1)
            self.cell(40, 10, row[2], 1, 0, 'R')
            self.cell(40, 10, row[3], 1, 1, 'R')

# Data Setup
transactions = [
    ["01-03-2026", "Opening Balance", "0.00", "50000.00"],
    ["05-03-2026", "Salary - Tata Motors", "+80000.00", "130000.00"],
    ["10-03-2026", "Rent Payment", "-15000.00", "115000.00"],
    ["12-03-2026", "UPI Transfer", "-2000.00", "113000.00"]
]

# Generate PDF
pdf = BankStatement()
pdf.add_page()
pdf.statement_details("Customer Name", "XXXX-XXXX-1234")
pdf.draw_table(transactions)
pdf.output("Bank_Statement.pdf")

print("Statement successfully generated: Bank_Statement.pdf")
