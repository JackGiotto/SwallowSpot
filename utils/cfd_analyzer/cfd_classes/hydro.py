import camelot
import json


class Hydro:
	
	# Number of the pages where date and risks can be collected
	PAGES_NUMBERS = {
		"date": "2",
		"risk": "2"
	}

	# the position in the table of the date
	DATE_POSITION = {
		"column": 3,
		"row": 1
	}

	data = {"type": "hydro"}

	def __init__(self, pdf_path):
		self.path = pdf_path
		self._get_bulletin_data()

	def get_data(self) -> dict:
		"""get date and risks of the bulletin
		"""

		return self.data

	def _get_bulletin_data(self):		
		print("Analyzing Htdro bulletin, path:", self.path)
		self.data["date"] = self._get_date(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["date"])[0].df)
		self.data["risks"] = self._get_risks(camelot.read_pdf(self.path, flavor='stream', pages=self.PAGES_NUMBERS["risk"])[0].df) 
		print("Finished analysis\n", json.dumps(self.data, indent="\t"))

	def _get_date(self, table) -> dict[str, str]:
		"""get the date of the bullettin
		"""
		
		string = table[self.DATE_POSITION["column"]][self.DATE_POSITION["row"]]
		splitted = string.split(' ')

		starting_date = splitted[2]
		starting_date += " " + splitted[4] + ":00" # add seconds to starting date
		
		ending_date = splitted[7]
		ending_date += " " + splitted[9]+ ":00"  # add seconds to ending date
		return {"starting_date": starting_date, "ending_date":ending_date}
		

	def _get_risks(self, table) -> dict[str, any]:
		"""get the value associated with every risk
		"""
		
		# risks template for hydro
		with open("utils/cfd_analyzer/templates/risks_template_hydro.json", "r") as f:
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
		with open("prova_hydro.json", "w") as f:
			json.dump(template, f, indent="\t")

# debug
hydro = Hydro("./test/data/test.pdf")