from utils.cfd_analyzer import cfd_classes
import camelot
import PyPDF2

class Pdf_reader:

	analyzer = None
	type = ""
	def __init__(self, path):
		pages = "2"
		with open(path, 'rb') as file:
			reader = PyPDF2.PdfFileReader(file)
			if reader.numPages == 1:
				pages="1"
			if reader.numPages == 4:
				pages="3"
			if reader.numPages == 6:
				pages="3"
		try:
			try:
				check = "PREVISTA" in camelot.read_pdf(path, flavor='stream', pages=pages)[0].df[2][0]
				table_number = 0
			except:
				print("strange pdf")
				check = "PREVISTA" in camelot.read_pdf(path, flavor='stream', pages=pages)[1].df[2][0]
				table_number = 1

			if (check):
				print("hydro")
				self.analyzer = cfd_classes.Hydro(path, pages, table_number)
				self.type = "hydro"
			else:
				print("snow")
				self.analyzer = cfd_classes.Snow(path, pages)
				self.type = "snow"
		except Exception as e:
			print(e)
			self.analyzer = None

	def get_cfd_data(self) -> dict[str, any]:
		data = self.analyzer.get_data()
		return data

	def print_table(self, path, pages):
		print("TABELLA\n", camelot.read_pdf(path, flavor='stream', pages=pages)[1].df)
		pass

	def add_to_db(self):
		self.analyzer.add_to_db()

# debug

#print(pdf.get_cfd_data())