from flask import Blueprint, render_template, request, session, redirect, url_for
from models import db
import hashlib


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
    cities_query = '''SELECT city_name, ID_city FROM Topology;'''
    cities = db.executeQuery(cities_query)
    print(cities)
    
    if request.method == "GET":
        if "username" not in session:
            # the user is not logged
            return render_template("auth/signup.html", cities=cities)
        else:
            # the user is logged
            return redirect(url_for("home.home"))
    elif request.method == "POST":
        # check if credential are correct
        username = request.form["username"]
        password = request.form["password"]
        password = _hash_password(password)
        city = request.form["city"]
        # zone = request.form["zone"]
        # confronto credenziali con DB
        
        sql = "SELECT username FROM User where username = '" + username + "';"
        result = db.executeQuery(sql)

        # check if username is already taken
        if bool(result):
            return render_template("auth/signup.html", msg="username non disponibile", cities = cities)
        else:
            ID_area_query = f''' SELECT Topology.ID_area 
                                FROM Topology
                                WHERE ID_city = {city}
                            '''
            ID_area = db.executeQuery(ID_area_query)
            print(ID_area)
            # save credentials into database
            db.executeQuery("INSERT INTO User (username, password, ID_area, ID_role) VALUES ('" + username + "', '" + password + "', " + str(ID_area[0]["ID_area"]) +", 1);")
            # start session
            session.permanent = True
            session["username"] = username
            print(session["username"])
            return redirect(url_for("home.home"))
    else:
        return render_template("auth/signup.html")
    
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
