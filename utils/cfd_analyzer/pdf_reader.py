import cfd_classes

PAGES_NUMBERS_HYDRO = {
	"date": "1",
	"risk": "2",
}

def get_cfd_data(path):
	mountain = cfd_classes.Mountain(path)
	
	# debug
	#print(data)


get_cfd_data("./test/data/test_mountain.pdf")