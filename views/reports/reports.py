from flask import Blueprint, render_template, redirect, url_for
from models import db
import json
from utils.risks import convert_risk_color, get_query_last_hydro, parse_date

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
            result[area]["risks"][risk] = convert_risk_color(bulletin["color_name"])
        result[area]["date"]["starting_date"] = parse_date(str(bulletin["starting_date"]))
        result[area]["date"]["ending_date"] = parse_date(str(bulletin["ending_date"]))


    return result

    # debug
    with open("prova.json", "w") as f:
        json.dump(result, f, indent="\t")


def _get_hydro_bulletin(area, risk, date):
    """get the risks of an area from a bulletin
    """
    
    if (date == 'last'):
        query = get_query_last_hydro(area, risk)
    return db.executeQuery(query)[0]