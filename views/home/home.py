from flask import Blueprint, render_template, session
from models import db

home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/')
def home():
    print (session)
    if "username" not in session:
        bulletin_data = '''
                    Per rimanere aggiornato sulla tua zona esegui l'accesso
                    <a href="/auth/login/" class="btn btn-success m-2 btn-lg"> Accedi</a>'''
    else:
        # debug
        #area_name = "Vene-A"
        hydraulic = "green"
        hydro_geo = "red"
        storms = "orange"
        update = "13-04-2024"

        # query to get user area
        query = f"""SELECT Area.area_name
                    FROM User
                    JOIN Area ON User.ID_area = Area.ID_area
                    WHERE User.username = '{session["username"]}';"""
        area_name = db.executeQuery(query)[0]["area_name"]

        hydraulic = db.executeQuery(_get_query(area_name, "idraulico"))[0]["color_name"]
        hydro_geo = db.executeQuery(_get_query(area_name, "idrogeologico"))[0]["color_name"]
        storms = db.executeQuery(_get_query(area_name, "idrogeologico con temporali"))[0]
        starting_date = storms["starting_date"]
        ending_date = storms["ending_date"]
        storms = storms["color_name"]

        bulletin_data = f'''<div class="risk-out" id="vene-a">
                                <h2>{area_name}</h2>
                                <p class="last-update" id="update-vene-a">Ultimo aggiornamento:<br>Data inizio: {_parse_date(str(starting_date))}<br>Data fine: {_parse_date(str(ending_date))}</p>
                                <div class="risk-in">
                                    <div class="risk">
                                        <span class="circle {_convert_risk_color(hydraulic)}"></span>
                                        <p>Rischio idraulico</p>
                                    </div>
                                    <div class="risk">
                                        <span class="circle {_convert_risk_color(hydro_geo)}"></span>
                                        <p>Rischio idro-geologico</p>
                                    </div>
                                    <div class="risk">
                                        <span class="circle {_convert_risk_color(storms)}"></span>
                                        <p>Rischio idro-geologico per temporale</p>
                                    </div>
                                </div>
                             </div>'''

    return render_template("home.html", bulletin_data = bulletin_data)

def _get_query(area_name, risk_name) -> str:
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

def _convert_risk_color(color) -> str:
    colors = {
        "verde": "green",
        "gialla": "yellow",
        "arancio": "orange",
        "rossa": "red"
    }
    return colors[color]

def _parse_date(date) -> str:
    date = date.split(" ")
    time = date[1]
    date = date[0]
    date = date.split("-")
    year = date[0]
    month = date[1]
    day = date[2]
    return day + "/" + month + "/" + year + " " + time[:-3]