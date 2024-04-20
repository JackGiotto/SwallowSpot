import camelot
import json

class Hydro:

	PAGES_NUMBERS = {
		"date": "1",
		"risk": "2"
	}

	DATE_POSITION = {
		"column": 1,
		"row": 0
	}

	data = {}

	def __init__(self, pdf_path):
		self.path = pdf_path
		#self.get_bulletin_data()

	def get_bulletin_data(self):
		self.data["date"] = self.get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"]))
		self.data["risks"] = self.get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])) 
   
	def get_date(self, table):
		string = table[0].df[self.DATE_POSITION["column"]][self.DATE_POSITION["row"]]
		splitted = string.split(' ')
		for single in splitted:
			if self.is_date(single):
				print("date", single)
				return single

		print("DATE NOT FOUND")

		return None

	def get_risks(self, table):
		with open("utils/cfd_analyzer/templates/risks_template_hydro.json", "r") as f:
			RISKS = json.load(f)
		table = table[0].df
		print(table)
		template = RISKS["risks_template"]
		for region, region_data in template.items():
			for risk, risk_value in region_data["risks_value"].items():
				template[region]["risks_value"][risk] = table[RISKS["risks_columns"][risk]][region_data["row"]]
			del region_data["row"]
		
		# debug
		#print(template)

		return template
		# debug
		with open("prova_hydro.json", "w") as f:
			json.dump(template, f, indent="\t")

	def is_date(self, string):
		return len(string) == 10 and string[2] == "/" and string[5] == "/"

# debug
#hydro = Hydro("./test/data/test.pdf")
