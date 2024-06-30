import camelot
import json
from utils.get_data import convert_date
from models import db
import PyPDF2
import os

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


	def _get_queries(self) -> dict:
		#print(self.data["risks"])
		queries = {"bulletin_query": "", "risks_queries": []}
		path = self.path

		if (os.getenv("start_path") != "./"):
			print("different")
			path = path.replace(os.getenv("start_path"), "./")

		queries["bulletin_query"] = f'''
					INSERT INTO Report(starting_date, ending_date, path) VALUES
					("{self.data["date"]["starting_date"]}", "{self.data["date"]["ending_date"]}", "{path}");
				'''
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
		return queries

	def _get_bulletin_data(self):		
		print("Analyzing Hydro bulletin, path:", self.path)

		self.data["date"] = self._get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"])[self.table_number].df)
		self.data["risks"] = self._get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])[self.table_number].df) 
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))

	def _get_date(self, table) -> dict[str, str]:
		"""get the date of the bullettin
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
		"""get the value associated with every risk
		"""
		
		# risks template for hydro
		with open(os.getenv("start_path") + "utils/cfd_analyzer/templates/risks_template_hydro.json", "r") as f:
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