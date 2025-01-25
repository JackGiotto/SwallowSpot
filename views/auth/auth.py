import os
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, make_response
from models import db
from utils.get_data import get_cities
from utils.password import hash_password, check_password
from utils.cookies_utils import add_permanent_cookie
from datetime import timedelta
import random
import string
import time
import sib_api_v3_sdk
from sib_api_v3_sdk import Configuration, ApiClient
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint

configuration = Configuration()
configuration.api_key['api-key'] = os.getenv["EMAILTOKEN"]

api_client = ApiClient(configuration)


BASE_SESSION_DURATION = 24 # hours
LONGER_SESSION_DURATION = 30 # days


auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if "username" not in session:
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
            resp = make_response(redirect(url_for("home.home")))
            if (result == 3):
                session["superadmin"] = 1
            if ("remember" in request.form):
                current_app.permanent_session_lifetime = timedelta(hours = BASE_SESSION_DURATION)
                resp = add_permanent_cookie(resp)
            else:
                current_app.permanent_session_lifetime = timedelta(hours = BASE_SESSION_DURATION)

            return resp
        else:
            # username does not exist or password is not correct =
            return render_template("auth/login.html", msg="Errore: Credenziali non corrette")
    else:
        return render_template("auth/login.html")

@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        if "username" not in session:
            return render_template("auth/signup.html")
        else:
            # the user is logged
            return redirect(url_for("home.home"))
    elif request.method == "POST": # signup
        # check if credential are correct
        username = request.form["username"]
        password = request.form["password"]
        email    = request.form["email"]
        if (username == ''):
            return render_template("auth/signup.html", msg="Errore: Il nome utente non può essere vuoto")
        if (len(password) < 8 or not has_number(password) or not has_uppercase(password) or not has_special_character(password)):
            return render_template("auth/signup.html", msg="Errore: La password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale")
        if (email == ''):
            return render_template("auth/signup.html", msg="Errore:  l'email non può essere vuota")
        
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
            db.executeQuery("INSERT INTO User (username, password, email, ID_area, ID_role) VALUES ('" + username + "', '" + password + "', '" + email + "'," + str(ID_area[0]["ID_area"]) +", 1);")
            # start session
            session.permanent = True
            session["username"] = username
            return redirect(url_for("home.home"))
        
@auth_bp.route('/email/', methods=['GET', 'POST'])
def recover_password():
    if request.method == "GET":
        return render_template("auth/recover_password.html")
    elif request.method == "POST": # signup
        # check if credential are correct
        username = request.form["username"]
        emailInsert = request.form["email"]
        if (username == ''):
            return render_template("auth/recover_password.html", msg="Errore: Il nome utente non può essere vuoto")
        
        sql = "SELECT email FROM User where username = '" + username + "';"
        result = db.executeQuery(sql)

        # check if username is already taken
        if bool(result):
              
            emailDB = result[0]['email']
            if(emailDB == emailInsert):
                length = 9
                random_string = generate_random_string(length) + "!"
                password = hash_password(random_string)
                ID_area_query = " UPDATE user SET `password` = '" + password + "' WHERE username = '" + username + "';"
                                
                ID_area = db.executeQuery(ID_area_query)
                if ID_area is not None: 
                    done = send_recovery_email(emailDB, random_string)
                    if(done):
                        return render_template("auth/login.html", success = "Email inviata con successo")
                    else:
                        return render_template("auth/recover_password.html", msg="Errore: email non inviata")
                else:
                    return render_template("auth/recover_password.html", msg="Errore: aggiornamento password fallito")
            else:
                return render_template("auth/recover_password.html", msg="I dati forniti non sono corretti. Verifica lo username e l'email inseriti e riprova.")

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def send_recovery_email(user_email, password):
    subject = "Recupero Password"
    html_content = f"""
    <html>
        <body>
            <h1>Ciao,</h1>
            <p>Hai richiesto di recuperare la tua password. Questa è la tua nuova password provvisoria: {password}</p>
        </body>
    </html>
    """
    sender = {"email": "swallowspottesting@gmail.com", "name": "SwallowSpot"}
    recipient = [{"email": user_email}]
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)

    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=recipient,
        sender=sender,
        subject=subject,
        html_content=html_content
    )
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(f"Email inviata a {user_email}: {api_response}")
        return True
    except ApiException as e:
        print(f"Errore nell'invio dell'email: {e}")
        return False