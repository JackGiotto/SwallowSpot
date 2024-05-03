from flask import Blueprint, render_template, redirect, session, url_for
import json

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