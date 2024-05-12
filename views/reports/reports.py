from flask import Blueprint, render_template, redirect, url_for, request
from models import db
import json
from utils.risks import convert_risk_color, get_query_last_hydro, get_query_hydro, get_query_snow, get_date_last_snow, parse_date_us_it, parse_date_it_us

reports_bp = Blueprint('reports', __name__, template_folder='templates')

@reports_bp.route('/hydro/', methods=['GET'])
def hydro():
    if not 'date' in request.args:
        return redirect(url_for("reports.hydro") + "?date=last")

    date = request.args['date']
    data = _get_all_bulletin_hydro(date)

    if date == "last":
        title = "Ultimo bollettino"
    else:
        title = "Bollettino del: " + date.replace("-", "/")


    if data == None:
        # redirect to error page
        pass

    return render_template("reports/hydro.html", data = data, title = title)

@reports_bp.route('/snow/', methods=['GET'])
def snow():
    if not 'date' in request.args:
        return redirect(url_for("reports.snow") + "?date=last")

    date = request.args['date']
    if date != 'last':
        print(date)
        title = "Bollettino del: " + date.replace("-", "/")
        date = parse_date_it_us(date + " 00:00:00")
        
    else:
        title = "Ultimo bollettino"
    print("date", date)
    data = _get_all_bulletin_snow(date)

    if data == None:
        # redirect to error page
        pass

    return render_template("reports/snow.html", data = data, title=title)

@reports_bp.route('/ava/')
def ava():
    return render_template("reports/ava.html")

@reports_bp.route('/')
def reports():
    return redirect(url_for("reports.hydro") + "?date=last")

def _get_all_bulletin_hydro(date = "last"):
    """get the risks of every area for an hydro bulletin
    """

    areas = ["Vene-A", "Vene-H", "Vene-B", "Vene-C", "Vene-D", "Vene-E", "Vene-F", "Vene-G"]
    risks = ["idraulico", "idrogeologico", "idrogeologico con temporali"]
    result = {
                "Vene-A": {
                    "date": {}, 
                    "risks": {}
                },
                "Vene-H": {
                    "date": {},
                    "risks": {}
                },
                "Vene-B": {
                    "date": {},
                    "risks": {}
                },
                "Vene-C": {
                    "date": {},
                    "risks": {}
                },
                "Vene-D":{
                    "date": {},
                    "risks": {}
                },
                "Vene-E": {
                    "date": {},
                    "risks": {}
                },
                "Vene-F": {
                    "date": {},
                    "risks": {}
                },
                "Vene-G": {
                    "date": {},
                    "risks": {}
                }
            }
    bulletin = None
    for area in areas:
        for risk in risks:
            bulletin = _get_hydro_bulletin(area, risk, date)
            result[area]["risks"][risk] = convert_risk_color(bulletin["color_name"])
        result[area]["date"]["starting_date"] = parse_date_us_it(str(bulletin["starting_date"]))
        result[area]["date"]["ending_date"] = parse_date_us_it(str(bulletin["ending_date"]))

    return result

    # debug
    with open("prova.json", "w") as f:
        json.dump(result, f, indent="\t")


def _get_hydro_bulletin(area: str, risk: str, date: str):
    """get the risks of an area from a hydro bulletin
    """
    
    if (date == 'last'):
        query = get_query_last_hydro(area, risk)
    else:
        query = get_query_hydro(area, risk, date)
    return db.executeQuery(query)[0]

def _get_all_bulletin_snow(date = "last") -> dict[str, dict[str, str]]:
    """get the risks of every area for a snow bulletin
    """ 

    areas = ["Alto Agordino", "Medio-basso Agordino", 'Cadore', 'Feltrino-Val Belluna', "Altopiano dei sette comuni"]
    print("data", date)
    if (date == "last"):
        date = get_date_last_snow()
    print("lamiabelladata", date)

    result = {
                "Alto Agordino": [],
                "Medio-basso Agordino": [],
                'Cadore' : [],
                'Feltrino-Val Belluna': [],
                'Altopiano dei sette comuni': []
            }
    bulletin = None
    for area in areas:
        bulletin = _get_snow_bulletin(area, date)
        if bulletin == None:
            return None
        result[area] = bulletin
        
    return result
    

def _get_snow_bulletin(area: str, date: str) -> list[dict[str,str]]:
    """get the risks of an area from a snow bulletin
    """

    query = get_query_snow(area, date)
    data = db.executeQuery(query)
    if (len(data) == 0):
        return None
    risks = [{}, {}, {}, {}, {}, {}, {}, {}, {}]
    i=0
    for row in data:

        risks[i] = _parse_row_snow(row)
        i += 1
    return risks

def _parse_row_snow(row: str) -> dict[str, str]:
    """parse a row obtained by Snow_report do a dictionary
    """

    new_risk = {}
    new_risk["date"] = parse_date_us_it(str(row['date']))
    new_risk["value"] = str(row['value'])
    new_risk["percentage"] = str(row['percentage'])
    return new_risk