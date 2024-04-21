import camelot
import json

class Mountain:
	PAGES_NUMBERS = {
		"date": "1",
		"risk": "1"
	}

	DATE_POSITION = {
		"column": 3,
		"row": 0
	}

	data = {"type": "mountain"}

	def __init__(self, pdf_path):
		self.path = pdf_path
		#self.get_bulletin_data()

	def get_bulletin_data(self):
		print("Analyzing Mountain bulletin, path:", self.path)
		self.data["date"] = self.get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"]))
		self.data["risks"] = self.get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])) 
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))

	def get_date(self, table):
		string = table[0].df[self.DATE_POSITION["column"]][self.DATE_POSITION["row"]]
		splitted = string.split(' ')
		date = self.parse_date(splitted)
		print(date)
		return date

	def get_risks(self, table):
		with open("utils/cfd_analyzer/templates/risks_template_mountain.json", "r") as f:
			RISKS = json.load(f)
		
		table = table[0].df
		print(table)
		template = RISKS["risks_template"]
		for mountain, mountain_data in template.items():
			for region, region_data in mountain_data.items():
				template[mountain][region]["risk_value"] = table[RISKS["risk_column"]][region_data["row"]]
			del region_data["row"]
		
		# debug
		#print(template)

		return template
		# debug
		with open("prova_mountain.json", "w") as f:
			json.dump(template, f, indent="\t")

	def parse_date(self, date_string):	
		with open("./utils/cfd_analyzer/templates/month_numbers.json", "r") as f:
			MONTH_NUMBERS = json.load(f)
		day = date_string[2]
		month = date_string[3]
		year=date_string[4]
		hour=date_string[6]

		return day + "-" + MONTH_NUMBERS[month] + "-" + year + " " + hour + ":00"
# debug
#mountain = Mountain("./test/data/test_mountain.pdf")