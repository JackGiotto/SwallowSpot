import camelot
import json

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

	data = {"type": "avalanches"}

	def __init__(self, pdf_path) -> None:
		self.path = pdf_path
		self._get_bulletin_data()

	def get_data(self) -> dict:
		"""get date and risks of the bulletin
		"""

		return self.data

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
		date = date.replace("/", "-") + " 00:00:00"
		return date
# debug
#snow = Snow("./test/data/test_snow.pdf")