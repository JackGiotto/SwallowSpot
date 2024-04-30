import cfd_classes
import camelot

class Pdf_reader:

	analyzer = None

	def __init__(self, path):
		if ("PREVISTA" in camelot.read_pdf(path, flavor='stream', pages="2")[0].df[2][0]):
			self.analyzer = cfd_classes.Hydro(path)
		else:
			self.analyzer = cfd_classes.Snow(path)

	def get_cfd_data(self) -> dict[str, any]:
		data = self.analyzer.get_data()
		return data


	def print_table(path):
		print(camelot.read_pdf(path, flavor='stream', pages="2")[0].df[2])
		pass


# debug

#pdf = Pdf_reader("./test/data/test_snow.pdf")
#print(pdf.get_cfd_data())