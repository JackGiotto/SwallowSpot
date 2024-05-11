from flask import Blueprint, render_template, redirect, session, request, url_for
from models import db
from utils.password import hash_password, has_uppercase, has_number, has_special_character
from utils.get_data import get_cities
import os
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
        if request.method == "GET":
            show_button = id_role>1
            return render_template("user/profile.html",  username=session["username"], user_perms=id_role, show_button=show_button)


        elif request.method == "POST":
            if "new_username" in request.form:
                new_username = request.form["new_username"]
                result = db.executeQuery("SELECT username FROM User where username = '" + new_username+ "';")
                # check if username is already taken
                if bool(result):
                    return render_template("user/profile.html", msg="username non disponibile", username=session["username"])
                else:
                    db.executeQuery("UPDATE User SET username = '"+str(new_username)+"' WHERE ID_user = '"+str(id_user)+"';")
                    session["username"] = new_username
                    return render_template("user/profile.html", username=session["username"])
                    


            elif "city" in request.form:
                new_zone = request.form["city"]
                if new_zone not in get_cities(want_list=True):
                    return render_template("user/profile.html", username=session["username"], msg="Errore: Il comune inserito non è valido")
                
                new_zone = db.executeQuery("SELECT Topology.ID_area FROM Topology WHERE Topology.city_name = '"+str(new_zone)+"';")
                new_zone= new_zone[0]["ID_area"]
                db.executeQuery("UPDATE User SET ID_area = "+str(new_zone)+" WHERE ID_user = "+str(id_user)+";")
                return render_template("user/profile.html", username=session['username'])

            elif "new_password" in request.form:
                new_password = request.form["new_password"]
                #checks password
                if (len(new_password) < 8 or not has_number(new_password) or not has_uppercase(new_password) or not has_special_character(new_password)):
                    print("Length condition or case condition or special character condition or number condition is met")
                    return render_template("user/profile.html", msg2="Errore: La password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale", username=session["username"])
                #hasing password
                new_password=hash_password(new_password)
                db.executeQuery("UPDATE User SET password = '"+str(new_password)+"' WHERE ID_user = '"+str(id_user)+"';")
                return render_template("user/profile.html", username=session['username'])
            
            elif "passwordDelete" in request.form:
                password = request.form['passwordDelete']
                print(password)
                password = hash_password(password)
                sql = "SELECT username, password FROM User where username = '" + session["username"] + "' and password = '" + password +"';"
                result = db.executeQuery(sql)
    
                #confronto e reindirizzamento
                if bool(result):
                    username = session["username"]
                    session.clear()
                    db.executeQuery("DELETE FROM `User` WHERE `username` = '"+str(username)+"'")
                    return redirect(url_for("home.home"))
                else:
                    return render_template("user/profile.html", msgpsw="Errore: password non corretta", username = session["username"])
                #db.executeQuery("DELETE FROM `User` WHERE ((`ID_user` = '"+str(id_user)+"'))")

        return render_template("user/profile.html")
    else:
        return render_template("user/settings.html")

@profile_bp.route('/profile/logout/', methods=['POST'])
def logout():
    session.clear()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}