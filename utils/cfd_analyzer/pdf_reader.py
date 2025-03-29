from utils.cfd_analyzer import cfd_classes
import camelot
import PyPDF2
import json


class Pdf_reader:

	analyzer = None
	type = ""
	def __init__(self, path):
		pages = "2"
		# wind_or_snow = self._check_wind_or_snow(pages, path)
		# if (wind_or_snow == 1):
		# 	print("wind")
		# 	self.analyzer = cfd_classes.Wind(path, pages)
		# 	self.type = "wind"
		# 	return
		# elif (wind_or_snow == 2):
		# 	print("non-mountain snow")
		# 	self.analyzer = cfd_classes.NonMountainSnow(path, pages)
		# 	self.type = "non mountain snow"
		# 	return
		# else:
		with open(path, 'rb') as file:
			reader = PyPDF2.PdfFileReader(file)
			if reader.numPages == 1:
				pages = "1"
			if reader.numPages == 4:
				pages = "3"
			if reader.numPages == 5:
				pages = "2"
			if reader.numPages == 6:
				pages = "3"
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

	def add_to_db(self):
		self.analyzer.add_to_db()

	def _check_wind_or_snow(self, pages, path) -> int:

		with open(path, "rb") as file:
			reader = PyPDF2.PdfReader(file)
			text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

		print(text)
		try:
			table = camelot.read_pdf(path, flavor='stream', pages=pages)[0].df[0]
			#print (table)
			for row in table:
				#print ("-----------------------------------------\n",row)
				if ("Vento FORTE" in row):
					# print("vento trovato")
					return 1
				elif ("per Nevicate" in row):
					# print ("nevicate trovate")
					return 2

		except:
			print ("ripperoni")
			return 0
		print("no")
		return 0

# debug

#print(pdf.get_cfd_data())


