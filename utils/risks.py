def get_query_last(area_name, risk_name) -> str:
    """get query for the last bulletin
    """

    query = f"""SELECT Report.starting_date, Report.ending_date, Color.color_name
            FROM Report
            JOIN Report_criticalness ON Report.ID_report = Report_criticalness.ID_report
            JOIN Criticalness ON Report_criticalness.ID_issue = Criticalness.ID_issue
            JOIN Area ON Criticalness.ID_area = Area.ID_area
            JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
            JOIN Color ON Criticalness.ID_color = Color.ID_color
            WHERE Area.area_name = '{area_name}' and Risk.risk_name = '{risk_name}'
            ORDER BY Report.ID_report DESC
            LIMIT 1;
        """
    return query

def parse_date(date) -> str:
    date = date.split(" ")
    time = date[1]
    date = date[0]
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]
    return day + "/" + month + "/" + year + " " + time[:-3]

def convert_risk_color(color) -> str:
    colors = {
        "verde": "green",
        "gialla": "yellow",
        "arancio": "orange",
        "rossa": "red"
    }
    return colors[color]