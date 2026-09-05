import os
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'PocketLedger: The Mamzo User Journey', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, points):
        self.set_font('Arial', '', 11)
        for point in points:
            self.multi_cell(0, 7, chr(149) + " " + point)
            self.ln(2)
        self.ln(2)
        
    def add_image(self, img_path, w=80):
        if os.path.exists(img_path):
            # center the image
            x = (210 - w) / 2
            self.image(img_path, x=x, w=w)
            self.ln(5)

pdf = PDF()
pdf.add_page()
base_path = r'C:\Users\shaba\.gemini\antigravity-ide\brain\bb9564dd-3ca1-48e3-a5ad-87714f99fc5f\.user_uploaded'

# Intro
pdf.chapter_title('Introduction & The Problem')
pdf.chapter_body([
    "Millions of informal micro-enterprises operate entirely in cash and leave no digital trace.",
    "Because they are functionally invisible, working capital and supplier financing are denied.",
    "PocketLedger wraps a financial-recording layer around WhatsApp, turning informal transactions into a trusted financial identity."
])

# Menu
pdf.chapter_title('1. The Accessible Interface (The Main Menu)')
pdf.chapter_body([
    "Mamzo doesn't need to download a new app; she uses WhatsApp.",
    "She interacts with a simple, numbered menu.",
    "Options include logging sales, logging stock, getting statements, and checking her Health Score."
])
# Add menu image (media_1788644550098.jpg or similar)
pdf.add_image(os.path.join(base_path, 'media_1788644550098.jpg'), w=60)

# Language
pdf.add_page()
pdf.chapter_title('2. Breaking Language Barriers')
pdf.chapter_body([
    "Inclusivity means speaking the merchant's language.",
    "By replying '7', Mamzo accesses a list of 18 African and international languages.",
    "She selects 'L2' for isiZulu, ensuring she isn't excluded by literacy or language barriers."
])
pdf.add_image(os.path.join(base_path, 'media_1788644549929.jpg'), w=60)

# Logging Sale
pdf.add_page()
pdf.chapter_title('3. Logging a Sale & Building the Health Score')
pdf.chapter_body([
    "To log a sale, Mamzo types naturally: 'I sold 10 tomatoes for R10 each'.",
    "PocketLedger's AI instantly parses this into structured financial data.",
    "It returns her Evidence Score and Health Score instantly.",
    "Every transaction proves her business is active, building her dynamic credit rating."
])
pdf.add_image(os.path.join(base_path, 'media_1788644549788.jpg'), w=60)

# Invoice
pdf.add_page()
pdf.chapter_title('4. Professionalizing with Digital Invoices')
pdf.chapter_body([
    "The bot generates a digital invoice link for every transaction.",
    "Mamzo clicks the link to see a clean, professional PDF Invoice for her customer.",
    "This creates a digital footprint of the transaction and provides professional customer service."
])
pdf.add_image(os.path.join(base_path, 'media_1788644549646.jpg'), w=80)

# Blockchain
pdf.chapter_title('5. Trust, Evidence, and Blockchain Anchoring')
pdf.chapter_body([
    "PocketLedger uses a multi-layered trust engine.",
    "AI Vision scans supplier receipts to verify stock purchases.",
    "Crucially, every validated transaction is cryptographically hashed and anchored on-chain.",
    "A lender looking at her Financial Identity Passport knows the data is immutable and hasn't been altered."
])

# Vision
pdf.chapter_title('6. The Bigger Vision: Bankability')
pdf.chapter_body([
    "Mamzo can pull a full financial statement showing revenue, expenses, and net profit.",
    "When applying for a micro-loan, she shares this verified Financial Identity Passport.",
    "For the first time, lenders see her verified cash flow and blockchain-backed evidence score.",
    "Mamzo is no longer invisible - she is a bankable business."
])

pdf.output('C:\\Users\\shaba\\.gemini\\antigravity-ide\\brain\\bb9564dd-3ca1-48e3-a5ad-87714f99fc5f\\PocketLedger_User_Journey.pdf')
