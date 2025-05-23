import camelot
import json
from utils.get_data import convert_date
from models import db
import os
import base64
import os
import base64
import PyPDF2

class Hydro:


	# the position in the table of the date
	DATE_POSITION = {
		"column": 3,
		"row": 1
	}

	PAGES_NUMBERS = {}

	data = {"type": "hydro"}

	def __init__(self, pdf_path, pages, table_number = 0):
		self.path = pdf_path
		print("path" + self.path)
		self.PAGES_NUMBERS["date"] = pages
		self.PAGES_NUMBERS["risk"] = pages
		self.table_number = table_number
		if (os.getenv("start_path") != "./"):
			self.template_path = os.getenv("start_path") + "utils/cfd_analyzer/templates/risks_template_hydro.json"
		else:
			self.template_path = "utils/cfd_analyzer/templates/risks_template_hydro.json"
		self._get_bulletin_data()

	def get_data(self) -> dict:
		"""get date and risks of the bulletin
		"""

		return self.data

	def add_to_db(self) -> None:
		last_index = "SELECT LAST_INSERT_ID() AS new_id;"
		queries = self._get_queries()

		# Execute the first query to insert the report
		report_query = queries["bulletin_query"]
		first_query = [report_query, last_index]
		report_id = db.executeTransaction(first_query, select=True)["new_id"]

		# debug
		print("Report ID:", report_id)

		# Loop through the risk queries
		for risk_query in queries["risks_queries"]:
			# Execute the risk query
			risk_query.append(last_index)
			risk_query[3] = risk_query[3].replace("@ID_report", str(report_id))
			db.executeTransaction(risk_query, select=False)

			# debug
			#print("RISK QUERY:", risk_query)

	def _get_bulletin_data(self):
		print("Analyzing Hydro bulletin, path:", self.path)

		self.data["date"] = self._get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"])[self.table_number].df)
		self.data["risks"] = self._get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])[self.table_number].df)
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))


	def _get_queries(self) -> dict:
		"""Generates SQL queries for inserting bulletin and risk data into the database.
		This method reads a PDF file, extracts specific pages, encodes the content in base64,
		and constructs SQL queries for inserting the bulletin data and associated risk data
		into the database.
		Returns:
			dict: A dictionary containing the SQL queries. The dictionary has two keys:
				- "bulletin_query": A string containing the SQL query to insert the bulletin data.
				- "risks_queries": A list of strings, each containing an SQL query to insert risk data.
		"""

		#print(self.data["risks"])
		queries = {"bulletin_query": "", "risks_queries": []}
		path = self.path
		with open(path, "rb") as f:
			pdf_reader = PyPDF2.PdfFileReader(f)
			pdf_writer = PyPDF2.PdfFileWriter()
			pdf_writer.addPage(pdf_reader.getPage(int(self.PAGES_NUMBERS["risk"]) - 1))
			output_pdf_path = os.environ["start_path"] + "static/bulletins/" + "temp_output.pdf"
			with open(output_pdf_path, "wb") as output_pdf:
				pdf_writer.write(output_pdf)
			with open(output_pdf_path, "rb") as output_pdf:
				pdf_data = base64.b64encode(output_pdf.read()).decode('utf-8')
			os.remove(output_pdf_path)
			# pdf_data = f.read()

		"""
		if (os.getenv("start_path") != "./"):
			print("different")
			path = path.replace(os.getenv("start_path"), "./")
		"""

		queries["bulletin_query"] = f'''
					INSERT INTO Report(starting_date, ending_date, pdf_data) VALUES
					("{self.data["date"]["starting_date"]}", "{self.data["date"]["ending_date"]}", "{pdf_data}");
				'''
		#print(queries["bulletin_query"])
		for key, values in self.data["risks"].items():
			area_name = key
			risk_name = ""
			color_name = ""
			for key2, value in values["risks_value"].items():
				risk_name = key2.lower()
				color_name = value
				query = [f'''SET @ID_area := (SELECT ID_area FROM Area WHERE area_name = '{area_name}');''',
						f'''SET @ID_risk := (SELECT ID_risk FROM Risk WHERE risk_name = '{risk_name}');''',
						f'''SET @ID_color := (SELECT ID_color FROM Color WHERE color_name = '{color_name}');''',
						f'''INSERT INTO Criticalness(ID_area, ID_risk, ID_color, ID_report) VALUES (@ID_area, @ID_risk, @ID_color, @ID_report);''']
				queries["risks_queries"].append(query)
		#print(queries)
		return queries

	def _get_date(self, table) -> dict[str, str]:
		"""get the date of the bulletin
		"""
		print(table)
		string = table[self.DATE_POSITION["column"]][self.DATE_POSITION["row"]]
		splitted = string.split(' ')

		starting_date = convert_date(splitted[2])
		starting_date += " " + splitted[4] + ":00" # add seconds to starting date

		ending_date = convert_date(splitted[7])
		ending_date += " " + splitted[9]+ ":00"  # add seconds to ending date
		return {"starting_date": starting_date, "ending_date":ending_date}


	def _get_risks(self, table) -> dict[str, any]:
		"""Extracts and processes risk data from a given table based on a predefined template.
		Args:
			table (dict): A dictionary containing risk data for various regions.
		Returns:
			dict[str, any]: A dictionary with processed risk values for each region.
		The function performs the following steps:
		1. Loads a risk template from a JSON file specified by `self.template_path`.
		2. Iterates over each region and its associated risk data in the template.
		3. Updates the risk values in the template based on the provided table.
		4. Removes unnecessary information from the template.
		5. Returns the updated template containing the processed risk values.
		6 (optional). Create a file with the data collected.
		"""

		# risks template for hydro
		with open(self.template_path, "r") as f:
			RISKS = json.load(f)

		template = RISKS["risks_template"]
		for region, region_data in template.items():
			for risk, risk_value in region_data["risks_value"].items():
				# save risk value
				template[region]["risks_value"][risk] = table[RISKS["risks_columns"][risk]][region_data["row"]]

			# delete unnecessary information
			del region_data["row"]

		# debug
		#print(template)

		return template

		# debug
		with open("test_hydro.json", "w") as f:
			json.dump(template, f, indent="\t")

# debug
#hydro = Hydro("./bulletins/test.pdf")