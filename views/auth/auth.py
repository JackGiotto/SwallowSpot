from flask import Blueprint, render_template
import requests

auth_page = Blueprint('auth', __name__, template_folder = 'templates')


@auth_page.route('/login/', methods=['GET', 'POST'])
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

@auth_page.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("registration/signup.html")
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
            return render_template("registration/signup.html")