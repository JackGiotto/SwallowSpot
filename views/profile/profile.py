from flask import Blueprint, render_template, redirect, session, request, url_for
from models import db
import re
import hashlib
import json

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET','POST'])
def user():
    cities_query = '''SELECT city_name, ID_city FROM Topology;'''
    cities = db.executeQuery(cities_query)

    if "username" in session:
        id_user = db.executeQuery("SELECT ID_user FROM User WHERE username ='"+session["username"]+"';")
        id_user = id_user[0]["ID_user"]
        id_role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
        id_role = id_role[0]["ID_role"]
        print(id_role)
        if request.method == "GET":
            show_button = True if id_role>1 else False
            return render_template("user/profile.html", cities=cities, username=session["username"], user_perms=id_role, show_button=show_button)


        elif request.method == "POST":
            result = db.executeQuery("SELECT username FROM User where username = '" + session["username"] + "';")

            if "new_username" in request.form:
                # check if username is already taken
                if bool(result):
                    return render_template("user/profile.html", msg1="username non disponibile", cities = cities, username=session["username"])
                else:
                    new_username = request.form["new_username"]
                    db.executeQuery("UPDATE User SET username = '"+str(new_username)+"' WHERE ID_user = '"+str(id_user)+"';")
                    session["username"]=new_username
                    return render_template("user/profile.html", cities = cities, username=session["username"])
            

            elif "city" in request.form:
                new_zone = request.form["city"]
                new_zone = db.executeQuery("SELECT ID_area, ID_city FROM Topology WHERE ID_city = "+str(new_zone)+";")
                new_zone= new_zone[0]["ID_area"]
                print(new_zone)
                db.executeQuery("UPDATE User SET ID_area = "+str(new_zone)+" WHERE ID_user = "+str(id_user)+";")
                print('area è stata modificata')

            elif "new_password" in request.form:
                new_password = request.form["new_password"]
                #checks password
                if (len(new_password) < 8 or not _has_number(new_password) or not _has_uppercase(new_password) or not _has_special_character(new_password)):
                    print("Length condition or case condition or special character condition or number condition is met")
                    return render_template("user/profile.html", msg2="la password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale")
                #hasing password
                new_password=_hash_password(new_password)
                db.executeQuery("UPDATE User SET password = '"+str(new_password)+"' WHERE ID_user = '"+str(id_user)+"';")
            
            elif "delete_account" in request.form:
                db.executeQuery("DELETE FROM `User` WHERE ((`ID_user` = '"+str(id_user)+"'))")

        return render_template("user/profile.html")
    else:
        return render_template("user/settings.html")

@profile_bp.route('/profile/logout/', methods=['POST'])
def logout():
    session.clear()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

#route x ADMIN
@profile_bp.route('/profile/admin/', methods=['GET','POST'])
def admin():
    cities_query = '''SELECT city_name, ID_city FROM Topology;'''
    cities = db.executeQuery(cities_query)

    if "username" in session:
        id_user = db.executeQuery("SELECT ID_user FROM User WHERE username ='"+session["username"]+"';")
        id_user = id_user[0]["ID_user"]
        
        if request.method == "GET":
            return render_template("user/profile.html", cities=cities, username=session["username"])

        elif request.method == "POST":
            result = db.executeQuery("SELECT username FROM User where username = '" + session["username"] + "';")

            if "new_username" in request.form:
                # check if username is already taken
                if bool(result):
                    return render_template("user/profile.html", msg="username non disponibile", cities = cities, username=session["username"])
                else:
                    new_username = request.form["new_username"]
                    db.executeQuery("UPDATE User SET username = '"+str(new_username)+"' WHERE ID_user = '"+str(id_user)+"';")
                    session["username"]=new_username
                    return render_template("user/profile.html", cities = cities, username=session["username"])
            
            elif "city" in request.form:
                new_zone = request.form["city"]
                new_zone = db.executeQuery("SELECT ID_area, ID_city FROM Topology WHERE ID_city = "+str(new_zone)+";")
                new_zone= new_zone[0]["ID_area"]
                print(new_zone)
                db.executeQuery("UPDATE User SET ID_area = "+str(new_zone)+" WHERE ID_user = "+str(id_user)+";")
                print('area è stata modificata')
            
            elif "admin_section" in request.form:
                return render_template("user/admin_profile.html")

            elif "new_password" in request.form:
                new_password = request.form["new_password"]
                #checks password
                if (len(new_password) < 8 or not _has_number(new_password) or not _has_uppercase(new_password) or not _has_special_character(new_password)):
                    print("Length condition or case condition or special character condition or number condition is met")
                    return render_template("user/profile.html", msg="la password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale")
                #hasing password
                new_password=_hash_password(new_password)
                db.executeQuery("UPDATE User SET password = '"+str(new_password)+"' WHERE ID_user = '"+str(id_user)+"';")
            elif "user_delete" in request.form:
                db.executeQuery("DELETE FROM `User` WHERE ((`ID_user` = '"+str(id_user)+"'))")

        return render_template("user/profile.html")
        
    else:
        return redirect("/auth/login")


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
