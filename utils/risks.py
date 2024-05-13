from models import db

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
                JOIN Criticalness ON Report.ID_report = Criticalness.ID_report
                JOIN Area ON Criticalness.ID_area = Area.ID_area
                JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
                JOIN Color ON Criticalness.ID_color = Color.ID_color
                WHERE Area.area_name = '{area_name}' AND Risk.risk_name = '{risk_name}'
                ORDER BY starting_date DESC
                LIMIT 1;
            """
    return query

def get_query_hydro(area_name: str, risk_name: str, date: str) -> str:
    
    date += " 00:00:00"
    date = parse_date_it_us(date)
    date = date.split(" ")[0]
    query = f"""SELECT Report.starting_date, Report.ending_date, Color.color_name
                FROM Report
                JOIN Criticalness ON Report.ID_report = Criticalness.ID_report
                JOIN Area ON Criticalness.ID_area = Area.ID_area
                JOIN Risk ON Criticalness.ID_risk = Risk.ID_risk
                JOIN Color ON Criticalness.ID_color = Color.ID_color
                WHERE Area.area_name = '{area_name}' AND Risk.risk_name = '{risk_name}' AND Report.starting_date LIKE '{date}%'
                ORDER BY starting_date DESC
                LIMIT 1;
            """
    return query

def get_date_last_snow() -> str:
    """get the date of the last snow bulletin

    Returns:
        str: query
    """


    query = """
            SELECT Snow_report.date
            FROM Snow_report
            ORDER BY Snow_report.date DESC
            LIMIT 1;
    """
    date = db.executeQuery(query)[0]['date']
    return date

def get_query_snow(area_name: str, date: str) -> str:
    """get query for snow bulletin

    Args:
        area_name (str): name of the area
        date (str): date of the bullettin code

    Returns:
        str: query
    """

    query = f"""
                SELECT Snow_criticalness.date, Snow_criticalness_altitude.value, Snow_criticalness.percentage
                FROM Snow_report
                JOIN Snow_criticalness ON Snow_report.ID_snow_report = Snow_criticalness.ID_snow_report
                JOIN Area ON Snow_criticalness.ID_area = Area.ID_area
                JOIN Snow_criticalness_altitude ON Snow_criticalness.ID_snow_issue = Snow_criticalness_altitude.ID_snow_issue
                JOIN Altitude ON Altitude.ID_altitude = Snow_criticalness_altitude.ID_altitude

                WHERE Area.area_name = '{area_name}' AND Snow_report.date = '{date}';
            """
    return query


def parse_date_us_it(date: str) -> str:
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

def parse_date_it_us(date: str) -> str:
    """converts date from italian notation to american notation

    Args:
        date (str): date with american notation
    Returns:
        str: date with italian notation
    """
    date = date.replace("/", "-")
    date = date.split(" ")
    time = date[1]
    date = date[0]
    date = date.split("-")
    day = date[0]
    month = date[1]
    year = date[2]
    return year + "-" + month + "-" + day + " " + time