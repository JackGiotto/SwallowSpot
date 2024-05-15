# trasfer the information of every city from text to query
import re

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# CHANGE ID ASSOCIATED WITH REGION NAME
name_id = {
	"Vene-A": "Vene-A",
	"Vene-H": "Vene-H",
	"Vene-B": "Vene-B",
	"Vene-C": "Vene-C",
	"Vene-D": "Vene-D",
	"Vene-E": "Vene-E",
	"Vene-F": "Vene-F",
	"Vene-G": "Vene-G",
}

# CHANGE NAME FOR ENTITY'S ATTRIBUTES
attributes_name = "city, ID_area"
# ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

with open("./cities/cities.txt", "r") as f:
	string = f.read()

list = []

rows = string.split("\n")

for row in rows:
	split_string = re.split(r'\s{2,}', row)
	split_string = [word for word in split_string if word]
	print(split_string)
	list.append({"city": split_string[1], "area": name_id[split_string[3].replace(" ", "-")]})


print(list)

sql_command = "INSERT INTO topology(" + attributes_name + ")"

for element in list:
	sql_command += "\n\t"
	sql_command += '("' + element["city"] +  '", "' + element["area"] +  '"),'

sql_command = sql_command.rsplit(',', maxsplit=1)
sql_command = ";".join(sql_command)
with open("./cities/cities.sql", "w") as f:
	f.write(sql_command)