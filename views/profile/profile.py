from flask import Blueprint, render_template, redirect, session, url_for,request
import json
import pymysql
import os

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET'])
def user():
    if "username" in session:
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


