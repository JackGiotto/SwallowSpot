import camelot
from utils.get_data import convert_date
from models import db
import os
import base64
import PyPDF2
import json

class NonMountainSnow:
	data = {"type": "non-mountain snow"}

	def __init__(self, pdf_path, pages):
		self.pages = pages
		self.path = pdf_path
		self._get_bulletin_data()

	def add_to_db(self):
		queries = self._get_queries()
		db.executeQuery(queries, select=False)

	def _get_bulletin_data(self) -> None:
		print("Analyzing Wind bulletin, path:", self.path)
		self.data["date"] = self._get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.pages)[1].df[0])
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))


	def _get_date(self, table) -> dict[str, str]:
		for row in table:
			print ("-------------------------------------------------\n", row)
			words = row.split(" ")
			if (words[0] == "dalle" and words[1] == "ore"):
				hours_start = words[2] + ":00"
				date_start = words[4]
				hours_end = words[7] + ":00"
				date_end = words[9]
				date_start = convert_date(date_start, "/")
				date_end = convert_date(date_end, "/")

				return {
					"start": date_start + " " + hours_start,
					"end": date_end + " " + hours_end
				}
		return None

	def _get_queries(self) -> str:
		path = self.path
		with open(path, "rb") as f:
			pdf_reader = PyPDF2.PdfFileReader(f)
			pdf_writer = PyPDF2.PdfFileWriter()
			pdf_writer.addPage(pdf_reader.getPage(int(self.pages) - 1))
			output_pdf_path = os.environ["start_path"] + "static/bulletins/" + "temp_output.pdf"
			with open(output_pdf_path, "wb") as output_pdf:
				pdf_writer.write(output_pdf)
			with open(output_pdf_path, "rb") as output_pdf:
				pdf_data = base64.b64encode(output_pdf.read()).decode('utf-8')
			os.remove(output_pdf_path)
			# pdf_data = f.read()
		queries = f'''
			INSERT INTO wind_reports (starting_date, ending_date, pdf_data) VALUES ('{self.data["date"]["start"]}', '{self.data["date"]["end"]}', '{pdf_data}');
		'''
		return queries