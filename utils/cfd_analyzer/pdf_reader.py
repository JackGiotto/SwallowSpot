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
		try:
			if ("PREVISTA" in camelot.read_pdf(path, flavor='stream', pages=pages)[0].df[2][0]):
				self.analyzer = cfd_classes.Hydro(path, pages)
				self.type = "hydro"
			else:
				self.analyzer = cfd_classes.Snow(path, pages)
				self.type = "snow"
		except Exception as e:
			print(e)
			self.analyzer = None

	def get_cfd_data(self) -> dict[str, any]:
		data = self.analyzer.get_data()
		return data

	def print_table(self, path):
		print(camelot.read_pdf(path, flavor='stream', pages="2")[0].df[2])
		pass

	def add_to_db(self):
		self.analyzer.add_to_db()

# debug

#print(pdf.get_cfd_data())