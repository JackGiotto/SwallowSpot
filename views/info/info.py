from flask import Blueprint, render_template, redirect, session, url_for
import json

info_bp = Blueprint('info', __name__, template_folder='templates')

@info_bp.route('/info/', methods=['GET'])
def info():
    return render_template("info.html")