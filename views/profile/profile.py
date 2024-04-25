from flask import Blueprint, render_template

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET'])
def user():
    return render_template("user/profile.html")
