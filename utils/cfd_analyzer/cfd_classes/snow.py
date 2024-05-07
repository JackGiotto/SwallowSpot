import camelot
import json
from utils.get_data import convert_date
from models import db

class Snow:

	# Number of the pages where date and risks can be collected
	PAGES_NUMBERS = {
		"date": "2",
		"risk": "2"
	}

	# the position in the table of the date
	DATE_POSITION = {
		"column": 1,
	}

	data = {"type": "snow"}

	def __init__(self, pdf_path) -> None:
		self.path = pdf_path
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
			#print("RISK QUERY", risk_query[1])

			risk_query[1] = risk_query[1].replace("@ID_snow_report", str(report_id))
			#print("RISK QUERY Cambiata", risk_query[1])
			
			print("SLICE", risk_query[0:3])
			id_crit = db.executeTransaction(risk_query[0:3], select=True)["new_id"]

			risk_query[4] = risk_query[4].replace("@ID_snow_issue", str(id_crit))
			risk_query[6] = risk_query[6].replace("@ID_snow_issue", str(id_crit))
			risk_query[8] = risk_query[8].replace("@ID_snow_issue", str(id_crit))
			db.executeTransaction(risk_query[3:], select=False)

			# debug
			#print("RISK QUERY:", risk_query)

	def _get_queries(self) -> dict:
		queries = {"bulletin_query": "", "risks_queries": []}

		queries["bulletin_query"] = f'''
			INSERT INTO Snow_report(date, path) VALUES
			("{self.data["date"]}", "{self.path}");
		'''
		for key, values_list in self.data["risks"].items():
			area_name = key
			for values in values_list:
				print(values)
				date_criticalness = values["date"]
				percentage = values["%"]
				first = list(values.items())[2]
				second = list(values.items())[3]
				third = list(values.items())[4]
				query = [
							f"""SET @ID_area := (SELECT ID_area FROM Area WHERE area_name = '{area_name}');""",
							f"""INSERT INTO Snow_criticalness(date, percentage, ID_area, ID_snow_report) VALUES
							('{date_criticalness}', '{percentage}', @ID_area,  @ID_snow_report);""",
							f"""SELECT LAST_INSERT_ID() AS new_id FROM Snow_criticalness ;""",
							
							f"SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = '{first[0]}');",
							f"""INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
							(@ID_snow_issue, @ID_altitude, '{first[1]}');""",	
							f"SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = '{second[0]}');",
							f"""INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
							(@ID_snow_issue, @ID_altitude, '{second[1]}');""",
							f"SET @ID_altitude := (SELECT ID_altitude FROM Altitude WHERE height = '{third[0]}');",
							f"""INSERT INTO Snow_criticalness_altitude(ID_snow_issue, ID_altitude, value) VALUES
							(@ID_snow_issue, @ID_altitude, '{third[1]}');"""
						]
				queries["risks_queries"].append(query)
		return queries

	def _get_bulletin_data(self) -> None:
		print("Analyzing Snow bulletin, path:", self.path)
		self.data["date"] = self._get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"])[0].df)
		self.data["risks"] = self._get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])[0].df) 
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))

	def _get_date(self, table) -> dict[str, str]:
		"""get the date of the bullettin
		"""
		column = table[self.DATE_POSITION["column"]]
		date = ""
		for row in column:
			if row != "" and row != "Data":
				date = row
				break
		
		date = self._parse_date(date)
		return date

	def _get_risks(self, table) -> dict[str, any]:
		"""get the value associated with every risk
		"""
	
		with open("utils/cfd_analyzer/templates/risks_template_snow.json", "r") as f:
			RISKS = json.load(f)
		

		column_date = table[RISKS["rows"]["date"]]
		column_percent = table[RISKS["rows"]["%"]]
		column_first_value = table[RISKS["rows"]["first_value"]]
		column_second_value = table[RISKS["rows"]["second_value"]]
		column_third_value = table[RISKS["rows"]["third_value"]]
		template = RISKS["risks_template"]

		template = self._get_column_data(column_date, template, "Data", "date")
		template = self._get_column_data(column_percent, template, "%", "%")
		template = self._get_column_data_value(column_first_value, template, 0)
		template = self._get_column_data_value(column_second_value, template, 1)
		template = self._get_column_data_value(column_third_value, template, 2)

		return template
	
		# debug
		with open("test_snow.json", "w") as f:
			json.dump(template, f, indent="\t")
				
	def _get_column_data(self, column, template, searching, position) -> dict[str, any]:
		"""get the data of a single bulletin's column (date or %)
		"""
		areas = ["Alto Agordino", "Medio-Basso Agordino", "Cadore", "Feltrino-Val Belluna", "Altopiano dei sette comuni"]
		
		i = 0
		j = 0
		for row in column:
			if j > 4:
				break
			if row != "" and row != searching:  # checks that the cell contains value
				if position == "date":
					row = self._parse_date(row)
				template[areas[j]][i][position] = row
				i += 1
				if (i == 3):
					i = 0
					j = j+1
		return template

	def _get_column_data_value(self, column, template, value_number) -> dict[str, any]:
		"""get the data of a single bulletin's column (values)
		"""
		areas = ["Alto Agordino", "Medio-Basso Agordino", "Cadore", "Feltrino-Val Belluna", "Altopiano dei sette comuni"]
		values1 = ["1500 m", "2000 m", ">2000 m"]
		values2 = ["1000 m", "1500 m", ">1500 m"]

		using = values1

		i = 0
		j = 0
		for row in column:
			if j > 4:
				break
			if j == 2:
				using = values2
			if row != "" and row != using[value_number]:  # checks that the cell contains value
				template[areas[j]][i][using[value_number]] = row
				i += 1
				if i == 3:
					i = 0
					j = j+1
		return template
	
	def _parse_date(self, date:str) -> str:
		date = date.replace("/", "-")
		date = convert_date(date) + " 00:00:00"
		return date
# debug
#snow = Snow("./test/data/test_snow.pdf")