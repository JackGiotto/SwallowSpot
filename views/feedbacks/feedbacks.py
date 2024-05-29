from flask import Blueprint, render_template, redirect, session, url_for
from models import db
from utils.risks import convert_risk_color, get_query_last_hydro, parse_date_us_it
import json
from Datetime import Datetime as dt

feedbacks_bp = Blueprint('feedbacks', __name__, template_folder='templates')

@feedbacks_bp.route('/feedback/', methods=['GET', 'POST'])
def feedbacks():#charge the page
    if(request.method == 'GET'):
        return render_template("feedbacks.html")
    elif(request.method == 'POST'):
        #check if the user in sessioned and return his own role
        if "username" in session:
            role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
            role = role[0]["ID_role"]
        else:#else judge him like a normal user
            role = 1
        if "feedback" in request.form:
            #fetching the information's feedback
            object = request.form["object"]
            description = request.form["message"]
            #execution of the query on database
            db.executeQuery("INSERT INTO Feedback (object, description, date, validate, ID_role) VALUES('title of the feedback ("+object+")', "+description+", NOW(), false, "+role+");")

