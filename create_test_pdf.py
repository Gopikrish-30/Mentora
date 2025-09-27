from fpdf import FPDF

def create_test_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add some test content
    pdf.cell(200, 10, txt="Test PDF Document", ln=1, align='C')
    pdf.cell(200, 10, txt="", ln=1, align='L')
    pdf.multi_cell(0, 10, txt="This is a test PDF document created for testing the text extraction functionality. It contains some sample text that should be extracted and stored in the vector database. The text includes various topics like machine learning, artificial intelligence, and data science to test the similarity search functionality.")
    
    # Save the PDF
    pdf.output("test.pdf")

if __name__ == "__main__":
    create_test_pdf()