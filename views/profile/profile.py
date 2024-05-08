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

@profile_bp.route('/profile/insert_chat_id', methods=['GET', 'POST'])
def insert_chat_id():
        print("cd")
        db = pymysql.connect (
            host= os.getenv("SERVERNAME"),
            user= os.getenv("DBUSER"),
            password= os.getenv("PASSWORD"),
            database= os.getenv("DBNAME"),
            cursorclass=pymysql.cursors.DictCursor
        )
        # Creare un cursore per eseguire le query
        cursor = db.cursor()
        # Get the username/password associated with this tag
        chat_id = request.form["ChatID"]
        print("cd")
        # Recupera i dati inviati dal client
        username = session["username"]
        print("cd")
        # Esegue la query per aggiornare l'ID di chat nel database
        query = "UPDATE Admin SET ID_telegram = %s WHERE username = %s"% (chat_id, username) 
        print(query)
        cursor.execute(query, (chat_id, username))
        db.commit()