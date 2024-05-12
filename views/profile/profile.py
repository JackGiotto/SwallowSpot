from flask import Blueprint, render_template, redirect, session, request, url_for
from models import db
from utils.password import hash_password, has_uppercase, has_number, has_special_character
from utils.get_data import get_cities
import json
from utils.bulletins_utils import save_bulletin
from models import db

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

@profile_bp.route('/profile/admin/', methods=['GET'])
def admin():

    # checks if user is admin
    id_user = db.executeQuery("SELECT ID_user FROM User WHERE username ='"+session["username"]+"';")
    id_user = id_user[0]["ID_user"]
    id_role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
    id_role = id_role[0]["ID_role"]

    if id_role <= 1:
        return redirect(url_for("profile.user"))
    elif id_role > 2:
        backup = f"""
                    <h2 class="mt-3">Esegui un <span style="color: #00667C;">backup</span> del database</h2>
                    <div class="input-group mt-2">
                        <input type="text" class="form-control" id="bkpServerIP" placeholder="IP del server per backup">
                    </div>
                    <button type="button" class="btn btn-success btn-lg mt-2" id="backupBtn"><i class="fa-solid fa-arrow-rotate-right"></i> Esegui Backup</button>
                    <p class="mt-1">Il file di backup viene salvato (dove?)</p>
                """


    return render_template("user/admin_profile.html", super_admin = backup)

@profile_bp.route('/profile/insert_id', methods=['POST'])
def insert_id():    
    # Recupera il valore inserito dall'utente nell'input con name="ChatID"
    chat_id = str(request.form["ChatID"])
    group_id = str(request.form["GroupID"])
    # Recupera il nome utente dalla sessione
    username = session["username"]
    print("username",str(username))
    user_query = f"SELECT ID_user FROM User WHERE username = '{username}'"
    user_result = db.executeQuery(user_query)[0]

    if user_result:
        user_id = int(user_result["ID_user"])
        print("iduser",str(user_id))
        # Esegue la query per aggiornare l'ID di chat nel database
        query = f"INSERT INTO Admin (ID_user, ID_telegram,GroupID) VALUES ({user_id}, '{chat_id}','{group_id}')"
        print(query)
        db.executeQuery(query)
            # Chiudi la connessione al database

    # Ritorna una risposta di successo o reindirizza a una nuova pagina
    return render_template("user/admin_profile.html")

@profile_bp.route('/profile/new_admin', methods=['POST'])
def new_admin():
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
            return render_template("user/admin_profile.html", msg_error_user = f"Errore: puoi aggiungere agli admin solo utenti non admin")
    else:
        return render_template("user/admin_profile.html", msg_error_user = f"Username non trovato")

@profile_bp.route('/profile/new_bulletin', methods=['POST'])
def new_bulletin():
    result = save_bulletin(request.files['uploadReport'])
    if (result[0] == "-"):
        return render_template("user/admin_profile.html", upload_error = "Errore: il file inserito non è leggibile") 
    return render_template("user/admin_profile.html")
