import camelot
import json

class Hydro:

	PAGES_NUMBERS = {
		"date": "2",
		"risk": "2"
	}

	DATE_POSITION = {
		"column": 3,
		"row": 1
	}

	data = {"type": "hydro"}

	def __init__(self, pdf_path):
		self.path = pdf_path
		#self.get_bulletin_data()

	def get_bulletin_data(self):
		print("Analyzing Mountain bulletin, path:", self.path)
		self.data["date"] = self.get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"]))
		self.data["risks"] = self.get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])) 
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))

	def get_date(self, table):
		table = table[0].df
		string = table[self.DATE_POSITION["column"]][self.DATE_POSITION["row"]]
		splitted = string.split(' ')
		starting_date = splitted[2]
		starting_date += " " + splitted[4] + ":00"
		ending_date = splitted[7]
		ending_date += " " + splitted[9]+ ":00"
		return {"starting_date": starting_date, "ending_date":ending_date}
		

	def get_risks(self, table):
		with open("utils/cfd_analyzer/templates/risks_template_hydro.json", "r") as f:
			RISKS = json.load(f)
		table = table[0].df
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