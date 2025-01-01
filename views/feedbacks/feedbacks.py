from flask import Blueprint, render_template, session, request
from models import db
import json
from datetime import datetime as dt

feedbacks_bp = Blueprint('feedbacks', __name__, template_folder='templates')

@feedbacks_bp.route('/feedback/', methods=['GET', 'POST'])
def feedbacks():#charge the page
    if(request.method == 'GET'):
        return render_template("feedbacks.html")
    elif(request.method == 'POST'):
        # check if the user in sessioned and return his own role
        if "username" in session:
            role = db.executeQuery("SELECT ID_role FROM User WHERE username ='"+session["username"]+"';")
            role = role[0]["ID_role"]
        else: # else judge him like a normal user
            role = 1
        if "feedObject" in request.form:
            # fetching the information's feedback
            feedObject = request.form["feedObject"].replace("'", "")
            feedDesc = request.form["feedDesc"].replace("'", "")
            # execution of the query on database
            query = f'''
                        INSERT INTO feedback (object, description, date, validate, ID_role)
                        VALUES(
                        '{feedObject}', '{feedDesc}', NOW(), 0, {role}
                        );
                    '''
            db.executeQuery(query)
            return render_template("feedbacks.html", feedback_success = "Feedback inviato con successo")