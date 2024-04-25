import camelot
import json

class Avalanches:

	# Number of the pages where date and risks can be collected
	PAGES_NUMBERS = {
		"date": "1",
		"risk": "1"
	}

	# the position in the table of the date
	DATE_POSITION = {
		"column": 3,
		"row": 0
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
		print("Analyzing Avalanches bulletin, path:", self.path)
		self.data["date"] = self._get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"])[0].df)
		self.data["risks"] = self._get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])[0].df) 
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))

	def _get_date(self, table) -> dict[str, str]:
		"""get the date of the bullettin
		"""
		string = table[self.DATE_POSITION["column"]][self.DATE_POSITION["row"]]
		splitted = string.split(' ')
		date = self._parse_date(splitted)
		return date

	def _get_risks(self, table) -> dict[str, any]:
		"""get the value associated with every risk
		"""

		# risks template for avalanches
		with open("utils/cfd_analyzer/templates/risks_template_avalanches.json", "r") as f:
			RISKS = json.load(f)
		
		template = RISKS["risks_template"]
		for mountain, mountain_data in template.items():
			for region, region_data in mountain_data.items():
				# save risk value
				template[mountain][region]["risk_value"] = table[RISKS["risk_column"]][region_data["row"]]
				
				# delete unnecessary information
				del region_data["row"]
		
		# debug
		#print(template)

		return template
		# debug
		with open("test_avalanche.json", "w") as f:
			json.dump(template, f, indent="\t")

	def _parse_date(self, date_string) -> str:
		"""converts month name to month number
		"""

		with open("./utils/cfd_analyzer/templates/month_numbers.json", "r") as f:
			MONTH_NUMBERS = json.load(f)

		day = date_string[2]
		month = date_string[3]
		year=date_string[4]
		hour=date_string[6]

		return day + "-" + MONTH_NUMBERS[month] + "-" + year + " " + hour + ":00"
# debug
#avalanches = Avalanches("./test/data/test_avalanches.pdf")