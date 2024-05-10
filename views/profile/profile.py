from flask import Blueprint, render_template, redirect, session, request, url_for
from models import db
from utils.password import hash_password, has_uppercase, has_number, has_special_character
from utils.get_data import get_cities
import os
import json

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET','POST', 'DELETE'])
def user():
    cities_query = '''SELECT city_name, ID_city FROM Topology;'''
    cities = db.executeQuery(cities_query)

    if "username" in session:
        id_user = db.executeQuery("SELECT ID_user FROM User WHERE username ='"+session["username"]+"';")
        id_user = id_user[0]["ID_user"]
        if request.method == "GET":
            return render_template("user/profile.html", username=session["username"])

        elif request.method == "POST":
            if "new_username" in request.form:
                new_username = request.form["new_username"]
                sql = "SELECT username FROM User where username = '" + new_username + "';"
                result = db.executeQuery(sql)
                if bool(result):
                    return render_template("user/profile.html", username=session["username"], msg="username already taken")
                db.executeQuery("UPDATE User SET username = '"+str(new_username)+"' WHERE ID_user = '"+str(id_user)+"';")
                session["username"]=new_username
                
                return render_template("user/profile.html", username=session["username"])
            
                

            elif "city" in request.form:
                new_zone = request.form["city"]
                if new_zone not in get_cities(want_list=True):
                    return render_template("user/profile.html", username=session["username"], msg="Errore: Il comune inserito non è valido")
                
                new_zone = db.executeQuery("SELECT Topology.ID_area FROM Topology WHERE Topology.city_name = '"+str(new_zone)+"';")
                new_zone= new_zone[0]["ID_area"]
                print(new_zone, id_user)
                db.executeQuery("UPDATE User SET ID_area = "+str(new_zone)+" WHERE ID_user = "+str(id_user)+";")
                print('area è stata modificata')
                return render_template("user/profile.html", username=session['username'])

            elif "new_password" in request.form:
                new_password = request.form["new_password"]
                #checks password
                if (len(new_password) < 8 or not has_number(new_password) or not has_uppercase(new_password) or not has_special_character(new_password)):
                    print("Length condition or case condition or special character condition or number condition is met")
                    return render_template("user/profile.html", msg="la password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale")
                #hasing password
                new_password = hash_password(new_password)
                db.executeQuery("UPDATE User SET password = '"+str(new_password)+"' WHERE ID_user = '"+str(id_user)+"';")
            elif "passwordDelete" in request.form:
                password = request.form['passwordDelete']
                password = hash_password(password)
                sql = "SELECT username, password FROM User where username = '" + session["username"] + "' and password = '" + password +"';"
                result = db.executeQuery(sql)
                
                #confronto e reindirizzamento
                if bool(result):
                    session.clear()
                    db.executeQuery("DELETE FROM `User` WHERE ((`ID_user` = '"+str(id_user)+"'))")
                    
                else:
                    return render_template("user/profile.html", msg="password non corretta", username = session["username"])
                #db.executeQuery("DELETE FROM `User` WHERE ((`ID_user` = '"+str(id_user)+"'))")
        
        return render_template("user/profile.html")
        
    else:
        return render_template("user/settings.html")

@profile_bp.route('/profile/logout/', methods=['POST'])
def logout():
    session.clear()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@profile_bp.route('/profile/admin/', methods=['GET'])
def admin():
    return render_template("user/admin_profile.html")

@profile_bp.route('/profile/insert_id', methods=['POST'])
def insert_id():
    db = pymysql.connect(
        host=os.getenv("SERVERNAME"),
        user=os.getenv("DBUSER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DBNAME"),
        cursorclass=pymysql.cursors.DictCursor
    )
    
    # Creare un cursore per eseguire le query
    cursor = db.cursor()

    # Recupera il valore inserito dall'utente nell'input con name="ChatID"
    chat_id = str(request.form["ChatID"])
    group_id = str(request.form["GroupID"])
    # Recupera il nome utente dalla sessione
    username = session["username"]
    print("username",str(username))
    user_query = "SELECT ID_user FROM User WHERE username = %s"
    cursor.execute(user_query, (username,))
    user_result = cursor.fetchone()

    if user_result:
        user_id = int(user_result["ID_user"])
        print("iduser",str(user_id))
        # Esegue la query per aggiornare l'ID di chat nel database
        query = f"INSERT INTO Admin (ID_user, ID_telegram,GroupID) VALUES ({user_id}, '{chat_id}','{group_id}')"
        print(query)
        cursor.execute(query)
        db.commit()
            # Chiudi la connessione al database
    db.close()

    # Ritorna una risposta di successo o reindirizza a una nuova pagina
    return render_template("user/admin_profile.html")


