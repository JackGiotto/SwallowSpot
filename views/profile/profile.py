from flask import Blueprint, render_template, redirect, session, request, url_for, current_app
import json
from models import db
from utils.password import hash_password, has_uppercase, has_number, has_special_character
from utils.get_data import get_cities
from utils.bulletins_utils import save_bulletin
from utils.db_backup.client_backup import start_backup


profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET','POST'])
def user():
    if "username" in session:
        id_user = db.executeQuery("SELECT ID_user FROM User WHERE username ='"+session["username"]+"';")
        id_user = id_user[0]["ID_user"]
        id_role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
        id_role = id_role[0]["ID_role"]

        if request.method == "GET":
            show_button = id_role>1
            return render_template("user/profile.html",  username=session["username"], user_perms=id_role, show_button=show_button)


        elif request.method == "POST":
            if "new_username" in request.form: # username change
                new_username = request.form["new_username"]
                result = db.executeQuery("SELECT username FROM User where username = '" + new_username+ "';")
                # check if username is already taken
                if bool(result):
                    return render_template("user/profile.html", msg="username non disponibile", username=session["username"])
                else:
                    db.executeQuery("UPDATE User SET username = '"+str(new_username)+"' WHERE ID_user = '"+str(id_user)+"';")
                    session["username"] = new_username
                    return render_template("user/profile.html", username=session["username"])

            elif "city" in request.form: # city change
                new_zone = request.form["city"]
                if new_zone not in get_cities(want_list=True):
                    return render_template("user/profile.html", username=session["username"], msg="Errore: Il comune inserito non è valido")
                
                new_zone = db.executeQuery("SELECT Topology.ID_area FROM Topology WHERE Topology.city_name = '"+str(new_zone)+"';")
                new_zone= new_zone[0]["ID_area"]
                db.executeQuery("UPDATE User SET ID_area = "+str(new_zone)+" WHERE ID_user = "+str(id_user)+";")
                return render_template("user/profile.html", username=session['username'])

            elif "new_password" in request.form: # password change
                new_password = request.form["new_password"]
                old_password = request.form["old_password"]
                #checks password
                if old_password==new_password:
                    return render_template("user/profile.html", msg2="Errore: La password nuova non deve essere uguale alla password vecchia ", username=session["username"])
                old_password=hash_password(old_password)
                result=db.executeQuery("SELECT User.password FROM User WHERE password = '"+str(old_password)+"';")
                if not result:
                    return render_template("user/profile.html", msg2="Errore: La password vecchia non è corretta ", username=session["username"])
                if (len(new_password) < 8 or not has_number(new_password) or not has_uppercase(new_password) or not has_special_character(new_password)):
                    return render_template("user/profile.html", msg2="Errore: La password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale", username=session["username"])
                # hasing password
                new_password=hash_password(new_password)
                db.executeQuery("UPDATE User SET password = '"+str(new_password)+"' WHERE ID_user = '"+str(id_user)+"';")
                return render_template("user/profile.html", username=session['username'])
            
            elif "passwordDelete" in request.form: # delete account
                password = request.form['passwordDelete']
                password = hash_password(password)
                sql = "SELECT username, password FROM User where username = '" + session["username"] + "' and password = '" + password +"';"
                result = db.executeQuery(sql)

                if bool(result):
                    username = session["username"]
                    session.clear()
                    db.executeQuery("DELETE FROM `User` WHERE `username` = '"+str(username)+"'")
                    return redirect(url_for("home.home"))
                else:
                    return render_template("user/profile.html", msgpsw="Errore: password non corretta", username = session["username"])

        return render_template("user/profile.html")
    else:
        return render_template("user/settings.html")

@profile_bp.route('/profile/logout/', methods=['POST'])
def logout():
    session.clear()
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@profile_bp.route('/profile/admin/', methods=['GET'])
def admin():
    if ('username' not in session):
        return redirect(url_for("profile.user"))
    # checks if user is admin
    id_role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
    id_role = id_role[0]["ID_role"]

    if id_role <= 1:
        return redirect(url_for("profile.user"))
    elif id_role == 3:
        session["superadmin"] = 1

    return render_template("user/admin_profile.html", maintenance = current_app.config["MAINTENANCE"])

@profile_bp.route('/profile/insert_id', methods=['POST'])
def insert_id():    
    # user data
    chat_id = str(request.form["ChatID"])
    group_id = str(request.form["GroupID"])

    username = session["username"]
    user_query = f"SELECT ID_user FROM User WHERE username = '{username}'"
    user_result = db.executeQuery(user_query)[0]

    if user_result:
        user_id = int(user_result["ID_user"])
        # create a new admin row 
        query = f"INSERT INTO Admin (ID_user, ID_telegram,GroupID) VALUES ({user_id}, '{chat_id}','{group_id}')"
        db.executeQuery(query)
    return render_template("user/admin_profile.html")

@profile_bp.route('/profile/change_to_admin', methods=['POST'])
def change_to_admin():
    new_admin_username = request.form["newAdminUser"]
    query = f"""SELECT ID_role
                FROM User
                WHERE username = '{new_admin_username}';
            """
    result = db.executeQuery(query)
    if bool(result):
        id_role_new_user = result[0]["ID_role"]
        if (id_role_new_user == 1):
            query = f"""
                        UPDATE User
                        SET ID_role = 2
                        WHERE username = '{new_admin_username}'; 
                    """
            db.executeQuery(query)
            return render_template("user/admin_profile.html", msg_success_user = f"Aggiunto {new_admin_username} agli admin")
        else:
            return render_template("user/admin_profile.html", msg_error_user = f"Errore: Puoi aggiungere agli admin solo utenti non admin")
    else:
        return render_template("user/admin_profile.html", msg_error_user = f"Errore: Username non trovato")

@profile_bp.route('/profile/new_admin', methods=['POST'])
def new_admin():
    # check if credentials are correct
    new_admin_username = request.form["username"]
    password = request.form["new_password"]
    id_role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
    id_role = id_role[0]["ID_role"]

    if (new_admin_username == ''):
        # empty name
        return render_template("user/admin_profile.html", new_msg_error="Errore: Il nome utente non può essere vuoto")
    if (len(password) < 8 or not has_number(password) or not has_uppercase(password) or not has_special_character(password)):
        return render_template("user/admin_profile.html", new_msg_error="Errore: La password deve contenere almeno 8 caratteri, un numero, una maiuscola e un carattere speciale", role=id_role)
    
    password = hash_password(password)
    city = request.form["city"]
    if city not in get_cities(want_list=True):
        return render_template("user/admin_profile.html", new_msg_error="Errore: Il comune inserito non è valido")

    sql = "SELECT username FROM User where username = '" + new_admin_username + "';"
    result = db.executeQuery(sql)

    # check if username is already taken
    if bool(result):
        return render_template("user/admin_profile.html", new_msg_error="Errore: L'username inserito è già utilizzato da un altro utente")
    else:
        ID_area_query = f''' SELECT Topology.ID_area 
                            FROM Topology
                            WHERE Topology.city_name = "{city}"
                        '''
        ID_area = db.executeQuery(ID_area_query)
        # save credentials into database
        db.executeQuery("INSERT INTO User (username, password, ID_area, ID_role) VALUES ('" + new_admin_username + "', '" + password + "', " + str(ID_area[0]["ID_area"]) +", 2);")
        return render_template("user/admin_profile.html", new_msg_success="Account creato con successo")


@profile_bp.route('/profile/new_bulletin', methods=['POST'])
def new_bulletin():
    result = save_bulletin(request.files['uploadReport'])
    if ("Errore" in result):
        return render_template("user/admin_profile.html", upload_error = result) 
    return render_template("user/admin_profile.html", upload_success = "Bollettino aggiunto con successo")

@profile_bp.route('/profile/backup', methods=['POST'])
def backup():
    IP_address = request.form["bkpServerIP"]
    port_number = request.form["bkpServerPort"]
    print("backup " + IP_address + port_number)
    result = start_backup(IP_address, port_number)
    if 'Errore' in result:
        return render_template("user/admin_profile.html", ip_error = result)
    return render_template("user/admin_profile.html")