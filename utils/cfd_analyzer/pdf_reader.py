from utils.cfd_analyzer import cfd_classes
import camelot
from models import db

class Pdf_reader:

	analyzer = None

	def __init__(self, path):
		if ("PREVISTA" in camelot.read_pdf(path, flavor='stream', pages="2")[0].df[2][0]):
			self.analyzer = cfd_classes.Hydro(path)
		else:
			self.analyzer = cfd_classes.Snow(path)

	def get_cfd_data(self) -> dict[str, any]:
		data = self.analyzer.get_data()
		return data


	def print_table(self, path):
		print(camelot.read_pdf(path, flavor='stream', pages="2")[0].df[2])
		pass

	def add_to_db(self):
		last_index = "SELECT LAST_INSERT_ID() AS new_id;"
		queries = self.analyzer.get_queries()

		# Execute the first query to insert the report
		report_query = queries["bulletin_query"]
		first_query = [report_query, last_index]
		report_id = db.executeTransaction(first_query)["new_id"]
		
		# debug
		#print("Report ID:", report_id)

		# Loop through the risk queries
		for risk_query in queries["risks_queries"]:
			# Execute the risk query
			risk_query.append(last_index)
			
			
			risk_id = db.executeTransaction(risk_query)["new_id"]

			# debug
			#print("RISK QUERY:", risk_query)
			#print("Risk ID:", risk_id)

			# Insert into Report_criticalness table
			new_query = f'''
					INSERT INTO Report_criticalness(ID_issue, ID_report)
					VALUES ({risk_id}, {report_id})
			'''
			db.executeQuery(new_query)

# debug

#print(pdf.get_cfd_data())