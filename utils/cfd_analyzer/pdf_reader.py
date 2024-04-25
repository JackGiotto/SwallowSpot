import cfd_classes
import json

PAGES_NUMBERS_HYDRO = {
	"date": "1",
	"risk": "2",
}

def get_cfd_data(path):
	avalanches = cfd_classes.Avalanches(path)
	print(avalanches.get_data())
	# debug
	#print(data)


get_cfd_data("./test/data/test_avalanches.pdf")