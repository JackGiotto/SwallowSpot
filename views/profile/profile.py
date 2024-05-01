from flask import Blueprint, render_template, redirect, session

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET'])
def user():
    if "username" in session:
        return render_template("user/profile.html")
    else:
        return redirect("/auth/login")