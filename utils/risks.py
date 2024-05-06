def get_query_last_hydro(area_name: str, risk_name: str) -> str:
    """get the query for last hydro bulletin

    Args:
        area_name (str): Vene-A, Vene-B...
        risk_name (str): verde, gialla...
    Returns:
        str: query
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

def parse_date(date: str) -> str:
    """converts date from american notation to italian notation

    Args:
        date (str): date with american notation
    Returns:
        str: date with italian notation
    """
    date = date.split(" ")
    time = date[1]
    date = date[0]
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]
    return day + "/" + month + "/" + year + " " + time[:-3]

def convert_risk_color(color:str) -> str:
    """converts risk color to a color usable in html

    Args:
        color (str): verde, gialla...
    Returns:
        str: color usable in html
    """

    colors = {
        "verde": "green",
        "gialla": "yellow",
        "arancio": "orange",
        "rossa": "red",
        "viola": "purple"
    }
    return colors[color]