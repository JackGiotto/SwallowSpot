import os
import secrets
from flask import Blueprint, render_template, request, session, redirect, url_for, current_app, make_response
from models import db
from utils.get_data import get_cities
from utils.password import _has_number, _has_special_character, _has_uppercase, hash_password, check_password
from utils.cookies_utils import add_permanent_cookie
from datetime import timedelta
import random
import string
import time
import sib_api_v3_sdk
from sib_api_v3_sdk import Configuration, ApiClient
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from datetime import datetime

configuration = Configuration()
configuration.api_key['api-key'] = os.getenv("EMAILTOKEN")

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
        if (len(password) < 8 or not _has_number(password) or not _has_uppercase(password) or not _has_special_character(password)):
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

            # Inserisci l'utente senza email
            insert_user_query = ("INSERT INTO User (username, password, ID_area, ID_role) "
                                "VALUES (%s, %s, %s, %s);")
            db.executeQuery(insert_user_query, (username, password, ID_area[0]["ID_area"], 1))

            # Recupera l'ID dell'utente appena inserito
            ID_user = db.executeQuery("SELECT LAST_INSERT_ID() AS ID_user;")[0]["ID_user"]

            # Inserisci l'email nella tabella Tokens
            insert_email_query = ("INSERT INTO Tokens (email, ID_user) "
                                "VALUES (%s, %s);")
            db.executeQuery(insert_email_query, (email, ID_user))

            # Avvia la sessione
            session.permanent = True
            session["username"] = username
            return redirect(url_for("home.home"))
        
@auth_bp.route('/email/', methods=['GET', 'POST'])
def recover_password():
    if request.method == "GET":
        return render_template("auth/recover_password.html")
    elif request.method == "POST": # signup
        # check if credential are correct
        current_username = request.form["username"]
        session["username"] = current_username
        if (current_username == ''):
            return render_template("auth/recover_password.html", msg="Errore: Il nome utente non può essere vuoto")
        sql = "SELECT email FROM User where username = '" + current_username + "';"
        print(sql)
        result = db.executeQuery(sql)

        # check if username is already taken
        if bool(result):
            emailDB = result[0]['email']
            token = generate_token() 
            ora_corrente = datetime.now()
            nuova_ora = ora_corrente + timedelta(minutes=15)
            ID_user_query = f"SELECT ID_user,email FROM User WHERE username = '{current_username}';"
            print(ID_user_query)
            result = db.executeQuery(ID_user_query)
            if not result:
                return render_template("auth/recover_password.html", msg="Errore: nome utente inesistente")
            # Usa una query parametrizzata per aggiornare il database
            ID_user = result[0]['ID_user']
            email = result[0]['email']
            print(nuova_ora.strftime("%Y-%m-%d %H:%M:%S") + " token " + token + "username " + current_username)
            select_token_query = f"""
                SELECT TOKEN FROM Tokens WHERE ID_user = {ID_user};
            """
            print(select_token_query)
            select_token_result = db.executeQuery(select_token_query)
            if select_token_result and len(select_token_result) > 0:
                delete_token_query = f"""
                DELETE FROM Tokens WHERE ID_user = {ID_user};
                """
                print(delete_token_query)
                db.executeQuery(delete_token_query)
                
            insert_token_query = f"""
                INSERT INTO Tokens (TOKEN, expirationDateToken, ID_user)
                VALUES ('{token}', '{nuova_ora.strftime('%Y-%m-%d %H:%M:%S')}', '{ID_user}');
            """
            print(insert_token_query)
            result = db.executeQuery(insert_token_query)
            
            if result is not None:
                print("query fatta")
                done = send_recovery_email(email, token)
                if(done):
                    return render_template("auth/auth_password.html", success = "Email inviata con successo")
                else:
                    return render_template("auth/recover_password.html", msg="Errore: email non inviata")
            else:
                print("query non fatta")
                return render_template("auth/recover_password.html", msg="Errore: nome utente inesistente")

def send_recovery_email(user_email, token):
    subject = "Recupero Password SwallowSpot"
    html_content = f"""
    <html>
        <body>
            <h1>Ciao,</h1>
            <p>Hai richiesto di recuperare la tua password. ecco il codice di autenticazione per resettare la tua password</p>
            <p>{token}</p>
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

def generate_token():
    length=32
    characters = string.ascii_letters + string.digits  # Lettere maiuscole, minuscole e numeri
    token = ''.join(secrets.choice(characters) for _ in range(length))
    return token


@auth_bp.route('/reset_password/', methods=['GET', 'POST'])
def reset_password():
    password = request.form["password"]
    current_username = session["username"]
    ID_user_query = f"SELECT ID_user,email FROM User WHERE username = '{current_username}';"
    result = db.executeQuery(ID_user_query)
    if not result:
        return render_template("auth/recover_password.html", msg="Errore: nome utente inesistente")
    # Usa una query parametrizzata per aggiornare il database
    ID_user = result[0]['ID_user']
    new_password=hash_password(password)
    print(f"id_user: {ID_user} password: {password}")
    db.executeQuery("UPDATE user SET password = '"+str(new_password)+"' WHERE ID_user = '"+str(ID_user)+"';")
    result = db.executeQuery("SELECT ID_user FROM user WHERE password = '"+str(new_password)+"' and ID_user = '"+str(ID_user)+"';")
    if result:
        return render_template("auth/login.html", success = "cambio password avvenuto con successo")
    else:
        return render_template("auth/recover_password.html", msg="Errore: cambio password non avvenuto, riprova")
    

@auth_bp.route('/auth_password/', methods=['GET', 'POST'])
def auth_password():
    token = request.form["code_auth"]
    current_username = session["username"]
    ID_user_query = f"SELECT ID_user,email FROM User WHERE username = '{current_username}';"
    print(ID_user_query)
    result = db.executeQuery(ID_user_query)
    if not result:
        return render_template("auth/recover_password.html", msg="Errore: nome utente inesistente")
    # Usa una query parametrizzata per aggiornare il database
    ID_user = result[0]['ID_user']
    ora_corrente = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formatta la data e ora
    query = f"SELECT TOKEN FROM tokens WHERE TOKEN = '{token}' AND ID_user = '{ID_user}' AND expirationDateToken > '{ora_corrente}'"
    print(query)
    exists = db.executeQuery(query)
    if exists:
        query = f"DELETE FROM tokens WHERE TOKEN = '{token}' AND ID_user = '{ID_user}'"
        print(query)
        exists = db.executeQuery(query)
        return render_template("auth/reset_password.html", success="Codice corretto")
    else:
        return render_template("auth/recover_password.html", msg="Errore: tempo per cambio password scaduto o codice errato")
