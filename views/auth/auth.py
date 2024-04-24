from flask import Blueprint, render_template, request, session, redirect, url_for

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    elif request.method == "POST":
        pass

@auth_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")
    elif request.method == "POST":
        pass
