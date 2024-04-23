from flask import Flask, request, render_template, url_for, redirect, session
from datetime import timedelta
import pymysql.cursors

app = Flask(__name__)
app.config["DEBUG"] = True

app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "klosterpatia"

'''people = [
    {
        "id": 1,
        "name": "Aldo",
        "surname": "Bordignon",
        "phone": "347 1957028"
    },
    {
        "id": 2,
        "name": "Sara",
        "surname": "Rodriguez",
        "phone": "328 0281954"
    },
    {
        "id": 3,
        "name": "Manny",
        "surname": "Stone",
        "phone": "123 4567890"
    }
]'''

def executeQuery(query):
    connection = pymysql.connect(host = "localhost",
                                user = "s02551",
                                password = "Aiw9ph",
                                database = "s02551",
                                cursorclass = pymysql.cursors.DictCursor
                                )
    
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            res = cursor.fetchall()
            connection.commit()
            return res

applicationName = "Conzazz"

@app.route('/')
def home():
    return render_template("home.html", app=applicationName)

@app.route('/reports/hydro/')
def hydro():
    return render_template("reports/hydro.html")

@app.route('/reports/ava/')
def ava():
    return render_template("reports/ava.html")

@app.route('/reports/')
def reports():
    return redirect(url_for("hydro"))

'''@app.route('/contacts/', methods = ["GET", "POST"])
def contacts():
    if request.method == "GET":
        sql = "select * from Contacts"
        return render_template("contacts.html", people=executeQuery(sql))
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        phone = request.form["phone"]
        sql = f"INSERT INTO Contacts(name, surname, phone) VALUES ('{name}', '{surname}', '{phone}')"
        executeQuery(sql)
        return redirect(url_for("contacts"))
    
@app.route('/contacts/<int:id>/', methods = ["GET", "DELETE"])
def get_person(id):
    if request.method == "GET":
        sql = "select * from Contacts where id=" + str(id)
        person = executeQuery(sql)
        return render_template("contacts.html", people=[person])
        #for contact in people:
        #    if contact["id"] == id:
        #        return render_template("contacts.html", people=[contact])
        #return "no existing contact has this ID"
    elif request.method == "DELETE":
        sql = "DELETE FROM Contacts WHERE id =" + str(id)
        executeQuery(sql)
        return "Successfully removed a person"
'''

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("registration/login.html")
    elif request.method == "POST":
        #check if credential are correct
        username = request.form["username"]
        password = request.form["password"]
        if username == "pallante" and password == "sasso":
            #sessione
            session.permanent = True
            session["username"] = username
            return redirect(url_for("user"))
        else:
            return render_template("registration/login.html")

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("registration/register.html")
    elif request.method == "POST":
        #check if credential are correct
        username = request.form["username"]
        password = request.form["password"]
        if username == "pallante" and password == "sasso":
            #sessione
            session.permanent = True
            session["username"] = username
            return redirect(url_for("user"))
        else:
            return render_template("registration/register.html")

'''@app.route('/user/')
def user():
    #controllo sessione
    if "username" in session:
        return render_template("user.html", username = session["username"])
    else:
        return redirect(url_for("login"))
'''

@app.route('/user/')
def user():
    return render_template("profile.html")



if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=11551)