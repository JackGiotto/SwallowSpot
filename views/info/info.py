from flask import Blueprint, render_template, redirect, session, url_for
from models import db

info_bp = Blueprint('info', __name__, template_folder='templates')

@info_bp.route('/info/', methods=['GET'])
def info():
    if "username" in session:
        id_role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
        id_role = id_role[0]["ID_role"]
        show_admin = id_role > 1
    else:
        show_admin = False
    return render_template("info.html", show_admin=show_admin)