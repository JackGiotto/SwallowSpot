import pandas
import camelot

PAGES_NUMBERS = {
	"date": "1",
	"risk": "2",
}

def get_cfd_data(path):
	data = {}
	data["date"] = get_date(camelot.read_pdf(path, flavor='stream', pages=PAGES_NUMBERS["date"]))

def get_date(table):
	string = table[0].df[1][0]

	splitted = string.split(' ')

	for single in splitted:
		if isDate(single):
			return single
	return None

def isDate(string):
	return len(string) == 10 and string[2] == "/" and string[5] == "/"