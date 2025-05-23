from flask import Blueprint, render_template, session, request
from models import db
from utils.risks import convert_risk_color, get_query_last_hydro, parse_date_us_it
from utils.get_data import get_cities, get_bulletins_dates
import json

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def home():
    if "username" not in session:
        bulletin_data = '''
                    Per rimanere aggiornato sulla tua zona esegui l'accesso
                    <a href="/auth/login/" class="btn btn-success m-2 btn-lg"><i class="fa-solid fa-right-to-bracket"></i> Accedi</a>
                    '''
    else:
        # if user is logged, get the last hydro buelettin for their area

        # query to get user area
        query = f"""SELECT Area.area_name
                    FROM User
                    JOIN Area ON User.ID_area = Area.ID_area
                    WHERE User.username = '{session["username"]}';"""
        area_name = db.executeQuery(query)


        if bool(area_name):
            area_name = area_name[0]['area_name']
            hydraulic = db.executeQuery(get_query_last_hydro(area_name, "idraulico"))[0]["color_name"]
            hydro_geo = db.executeQuery(get_query_last_hydro(area_name, "idrogeologico"))[0]["color_name"]
            storms = db.executeQuery(get_query_last_hydro(area_name, "idrogeologico con temporali"))[0]
            starting_date = storms["starting_date"]
            ending_date = storms["ending_date"]
            storms = storms["color_name"]

            bulletin_data = f'''<div class="risk-out-home">
                                    <h2>{area_name}</h2>
                                    <p id="lastUpdate">Ultimo aggiornamento:<br>Data inizio: {parse_date_us_it(str(starting_date))}<br>Data fine: {parse_date_us_it(str(ending_date))}</p>
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
        else:
            bulletin_data = """Server error"""

    return render_template("home.html", bulletin_data = bulletin_data)

@home_bp.route('/cities', methods=['GET'])
def cities():
    cities = get_cities()
    return json.dumps({'success':True, 'cities': cities}), 200, {'ContentType':'application/json'}

@home_bp.route('/snake', methods=['GET'])
def snake():
    return render_template("snake.html")

@home_bp.route('/bulletins_dates', methods=['GET'])
def bulletins_dates():
    type_of_bulletin = request.args.get('type')
    bulletins_dates = get_bulletins_dates(type_of_bulletin)
    return json.dumps({'success':True, 'dates': bulletins_dates}), 200, {'ContentType':'application/json'}

@home_bp.route('/notification')
def notification():
    if "username" in session:
        query = f"""SELECT Area.area_name
                    FROM User
                    JOIN Area ON User.ID_area = Area.ID_area
                    WHERE User.username = '{session["username"]}';"""
        area_name = db.executeQuery(query)


        if bool(area_name):
            area_name = area_name[0]['area_name']
            hydraulic = db.executeQuery(get_query_last_hydro(area_name, "idraulico"))[0]["color_name"]
            hydro_geo = db.executeQuery(get_query_last_hydro(area_name, "idrogeologico"))[0]["color_name"]
            storms = db.executeQuery(get_query_last_hydro(area_name, "idrogeologico con temporali"))[0]

        result = {
            "hydro": hydraulic,
            "hydro_geo": hydro_geo,
            "storms": storms,
        }
        if 'storms' in result:
            result['storms'].pop('starting_date', None)
            result['storms'].pop('ending_date', None)

        return json.dumps({'success':True, 'result': result}), 200, {'ContentType':'application/json'}
    else:
        return "", 500
