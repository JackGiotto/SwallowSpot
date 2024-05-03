from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db
import json

reports_bp = Blueprint('reports', __name__, template_folder='templates')

@reports_bp.route('/hydro/')
def hydro():
    _get_all_bulletins()
    return render_template("reports/hydro.html", data = _get_all_bulletins())

@reports_bp.route('/snow/')
def snow():
    return render_template("reports/snow.html")

@reports_bp.route('/ava/')
def ava():
    return render_template("reports/ava.html")

@reports_bp.route('/')
def reports():
    return redirect(url_for("reports.hydro"))

def _get_all_bulletins(date = "last"):
    """get the risks of every area for a bulletin
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
            result[area]["risks"][risk] = _convert_risk_color(bulletin["color_name"])
        result[area]["date"]["starting_date"] = _parse_date(str(bulletin["starting_date"]))
        result[area]["date"]["ending_date"] = _parse_date(str(bulletin["ending_date"]))


    return result

    # debug
    with open("prova.json", "w") as f:
        json.dump(result, f, indent="\t")


def _get_hydro_bulletin(area, risk, date):
    """get the risks of an area from a bulletin
    """
    
    if (date == 'last'):
        query = _get_query_last(area, risk)
    return db.executeQuery(query)[0]


def _get_query_last(area_name, risk_name) -> str:
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

def _parse_date(date) -> str:
    date = date.split(" ")
    time = date[1]
    date = date[0]
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]
    return day + "/" + month + "/" + year + " " + time[:-3]

def _convert_risk_color(color) -> str:
    colors = {
        "verde": "green",
        "gialla": "yellow",
        "arancio": "orange",
        "rossa": "red"
    }
    return colors[color]