from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db
from utils.get_data import get_cities
import hashlib
import re


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
    elif request.method == "POST":#login
        username = request.form["username"]
        password = request.form["password"]
        password = _hash_password(password)
        # checks credentials with DB
        sql = "SELECT username, password FROM User where username = '" + username + "' and password = '" + password +"';"
        result = db.executeQuery(sql)
        
        #confronto e reindirizzamento
        if bool(result):
            # correct
            session.permanent = True
            session["username"] = username
            return redirect(url_for("home.home"))
        else:
            # username does not exist or password is not correct =
            return render_template("auth/login.html", msg="credenziali non corrette")
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
    elif request.method == "POST":
        # check if credential are correct
        username = request.form["username"]
        password = request.form["password"]

        if (username == ''):
            return render_template("auth/signup.html", msg="il nome utente non può essere vuoto")
        if (len(password) < 8 or not _has_number(password) or not _has_uppercase(password) or not _has_special_character(password)):
            print("Length condition or case condition or special character condition or number condition is met")
            return render_template("auth/signup.html", msg="la password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale")
        
        password = _hash_password(password)
        city = request.form["city"]
        if city not in get_cities(want_list=True):
            return render_template("auth/signup.html", msg="il comune inserito non è valido")
        # zone = request.form["zone"]
        # confronto credenziali con DB

        sql = "SELECT username FROM User where username = '" + username + "';"
        result = db.executeQuery(sql)

        # check if username is already taken
        if bool(result):
            return render_template("auth/signup.html", msg="username non disponibile")
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
    
def _hash_password(password):
    # Converte la password in una stringa di byte
    password_bytes = password.encode('utf-8')

    # Crea un oggetto hash SHA-256
    sha256_hash = hashlib.sha256()

    # Aggiunge la password alla funzione hash
    sha256_hash.update(password_bytes)

    # Ottieni l'hash crittografico in esadecimale
    hashed_password = sha256_hash.hexdigest()

    return hashed_password


def _has_uppercase(s):
    """Check if a string contains at least one uppercase letter.
    """
    return any(char.isupper() for char in s)

def _has_number(s):
    """Check if a string contains at least one number.
    """
    return any(char.isdigit() for char in s)

def _has_special_character(s):
    """Check if a string contains at least one special character.
    """
    special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    return special_characters.search(s) is not None