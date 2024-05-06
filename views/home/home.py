from flask import Blueprint, render_template, session
from models import db
from utils.risks import convert_risk_color, get_query_last_hydro, parse_date
from utils.get_data import get_cities
import json

home_bp = Blueprint('home', __name__, template_folder='templates')

@home_bp.route('/')
def home():
    print (session)
    if "username" not in session:
        bulletin_data = '''
                    Per rimanere aggiornato sulla tua zona esegui l'accesso
                    <a href="/auth/login/" class="btn btn-success m-2 btn-lg"><i class="fa-solid fa-right-to-bracket"></i> Accedi</a>'''
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

        hydraulic = db.executeQuery(get_query_last_hydro(area_name, "idraulico"))[0]["color_name"]
        hydro_geo = db.executeQuery(get_query_last_hydro(area_name, "idrogeologico"))[0]["color_name"]
        storms = db.executeQuery(get_query_last_hydro(area_name, "idrogeologico con temporali"))[0]
        starting_date = storms["starting_date"]
        ending_date = storms["ending_date"]
        storms = storms["color_name"]

        bulletin_data = f'''<div class="risk-out" id="vene-a">
                                <h2>{area_name}</h2>
                                <p class="last-update" id="update-vene-a">Ultimo aggiornamento:<br>Data inizio: {parse_date(str(starting_date))}<br>Data fine: {parse_date(str(ending_date))}</p>
                                <div class="risk-in">
                                    <div class="risk">
                                        <span class="circle {convert_risk_color(hydraulic)}"></span>
                                        <p>Rischio idraulico</p>
                                    </div>
                                    <div class="risk">
                                        <span class="circle {convert_risk_color(hydro_geo)}"></span>
                                        <p>Rischio idro-geologico</p>
                                    </div>
                                    <div class="risk">
                                        <span class="circle {convert_risk_color(storms)}"></span>
                                        <p>Rischio idro-geologico per temporale</p>
                                    </div>
                                </div>
                             </div>'''

    return render_template("home.html", bulletin_data = bulletin_data)


@home_bp.route('/cities', methods=['GET'])
def cities():
    cities = get_cities()
    return json.dumps({'success':True, 'cities': cities}), 200, {'ContentType':'application/json'}