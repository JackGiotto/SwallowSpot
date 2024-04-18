import camelot
import json

PAGES_NUMBERS = {
	"date": "1",
	"risk": "2",
}

def get_cfd_data(path):
	data = {}
	data["date"] = get_date(camelot.read_pdf(path, flavor='stream', pages=PAGES_NUMBERS["date"]))
	data["risks"] = get_risks(camelot.read_pdf(path, flavor='stream', pages=PAGES_NUMBERS["risk"])) 
	
	# debug
	#print(data)

def get_date(table):
	string = table[0].df[1][0]
	splitted = string.split(' ')
	for single in splitted:
		if is_date(single):
			return single
	return None

def get_risks(table):
	with open("utils/templates/risks_template.json", "r") as f:
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
	with open("prova.json", "w") as f:
		json.dump(template, f, indent="\t")

def is_date(string):
	return len(string) == 10 and string[2] == "/" and string[5] == "/"