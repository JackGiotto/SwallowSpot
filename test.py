from utils.cfd_analyzer.pdf_reader import Pdf_reader


pdf = Pdf_reader("./bulletins/test.pdf")
pdf.add_to_db()