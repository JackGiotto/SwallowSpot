from flask import Blueprint, render_template, redirect, session, url_for
import json

feedbacks_bp = Blueprint('feedbacks', __name__, template_folder='templates')

@feedbacks_bp.route('/feedback/', methods=['GET'])
def feedbacks():
    return render_template("feedbacks.html")