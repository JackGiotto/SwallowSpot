from flask import Blueprint, render_template, request, session, redirect, url_for
import pymysql.cursors

auth_bp = Blueprint('auth', __name__, template_folder='templates')

def executeQuery(query):
    connection = pymysql.connect(host = "localhost",
                                user = "s02675",
                                password = "Ohmah6",
                                database = "s02675",
                                cursorclass = pymysql.cursors.DictCursor
                                )
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
            connection.commit()
            return res

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":#accesso risorsa
        return render_template("auth/login.html")
    elif request.method == "POST":#login
        username = request.form["username"]
        password = request.form["password"]
        #confronto credenziali con DB
        sql = "CREATE VIEW UserView AS SELECT username,password,CASE WHEN username = '"+username+"' AND password = '"+password+"' THEN 'true' ELSE 'false' END AS user_exists FROM User;"
        executeQuery(sql)
        result = executeQuery("SELECT user_exists FROM UserView;")#restituisce lista-dizionario
        executeQuery("DROP VIEW UserView;")
        #confronto e reindirizzamento
        if(result[0]["user_exists"] == "true"):
            #stabilimento sessione
            session.permanent = True
            session["username"] = username
            return render_template("home.html")
        else:
            return render_template("auth/login.html", msg="credenziali non corrette")
    else:
        return render_template("auth/login.html")

@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")
    elif request.method == "POST":
        #check if credential are correct
        username = request.form["username"]
        password = request.form["password"]
        #zone = request.form["zone"]
        #confronto credenziali con DB
        sql = "CREATE VIEW UserView AS SELECT username,password,CASE WHEN username = '"+username+"' THEN 'true' ELSE 'false' END AS user_exists FROM User;"
        executeQuery(sql)
        result = executeQuery("SELECT user_exists FROM UserView;")#restituisce lista-dizionario
        executeQuery("DROP VIEW UserView;")
        #inserimento zone dsponibili
        listcity= executeQuery("SELECT city_name, ID_city FROM Toclearpology;")
        
        for i in listcity:
            html_code += f'<option name="zone">'+listcity[i]["ID_city"]+'</option>'

        #confronto e reindirizzamento
        if(result[0]["user_exists"] == "true"):#true -> utente gia presente nel db 
            return render_template("auth/signup.html", msg="username non disponibile")
        elif(result[0]["user_exists"] == "false"):#false -> utente non presente nel db
            #registrazione credenziali utente nel db -- MANCA ZONA DI RESIDENZA !!!!!
            executeQuery("INSERT INTO `User` (`username`, `password`, `ID_area`, `ID_role`)VALUES ('"+username+"', '"+password+"','5', '1');")
            #stabilimento sessione
            session.permanent = True
            session["username"] = username
            return redirect(url_for("profile.user"))
    else:
        return render_template("auth/signup.html")

