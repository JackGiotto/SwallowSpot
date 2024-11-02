from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from models import db
from utils.get_data import get_cities
from utils.password import hash_password, check_password
from datetime import timedelta



BASE_SESSION_DURATION = 24 # hours
LONGER_SESSION_DURATION = 30 # days


auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if "username" not in session:
            # the user is not logged
            return render_template("auth/login.html")
        else:
            # the user is logged
            return redirect(url_for("home.home"))
    elif request.method == "POST": # login
        username = request.form["username"]
        password = request.form["password"]
        password = hash_password(password)
        # checks credentials with DB
        sql = "SELECT username, password FROM User where username = '" + username + "' and password = '" + password +"';"
        result = db.executeQuery(sql)

        #confronto e reindirizzamento
        if bool(result):
            # correct
            session.permanent = True
            session["username"] = username
            sql = "SELECT ID_role FROM User WHERE username = '" + username + "'"
            result = db.executeQuery(sql)[0]["ID_role"]
            if (result == 3):
                session["superadmin"] = 1
            if ("remember" in request.form):
                current_app.permanent_session_lifetime = timedelta(days = LONGER_SESSION_DURATION)
            else:
                current_app.permanent_session_lifetime = timedelta(hours = BASE_SESSION_DURATION)
            return redirect(url_for("home.home"))
        else:
            # username does not exist or password is not correct =
            return render_template("auth/login.html", msg="Errore: Credenziali non corrette")
    else:
        return render_template("auth/login.html")

@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        if "username" not in session:
            # the user is not logged
            return render_template("auth/signup.html")
        else:
            # the user is logged
            return redirect(url_for("home.home"))
    elif request.method == "POST": # signup
        # check if credential are correct
        username = request.form["username"]
        password = request.form["password"]

        if (username == ''):
            return render_template("auth/signup.html", msg="Errore: Il nome utente non può essere vuoto")
        if (not check_password(password)):
            return render_template("auth/signup.html", msg="Errore: La password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale")

        password = hash_password(password)
        city = request.form["city"]
        if city not in get_cities(want_list=True):
            return render_template("auth/signup.html", msg="Errore: Il comune inserito non è valido")
        # zone = request.form["zone"]
        # confronto credenziali con DB

        sql = "SELECT username FROM User where username = '" + username + "';"
        result = db.executeQuery(sql)

        # check if username is already taken
        if bool(result):
            return render_template("auth/signup.html", msg="Errore: Username non disponibile")
        else:
            ID_area_query = f''' SELECT Topology.ID_area
                                FROM Topology
                                WHERE Topology.city_name = "{city}"
                            '''
            ID_area = db.executeQuery(ID_area_query)
            # save credentials into database
            db.executeQuery("INSERT INTO User (username, password, ID_area, ID_role) VALUES ('" + username + "', '" + password + "', " + str(ID_area[0]["ID_area"]) +", 1);")
            # start session
            session.permanent = True
            session["username"] = username
            return redirect(url_for("home.home"))