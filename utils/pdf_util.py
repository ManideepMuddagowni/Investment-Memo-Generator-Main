from fpdf import FPDF

def save_text_pdf(memo: str, filename: str = "memo.pdf") -> str:
    pdf = FPDF()
    pdf.add_page()

    # Add a Unicode font
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font('DejaVu', '', 12)

    # Split memo into lines and add each line to the PDF
    for line in memo.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename
