from flask import Blueprint, render_template, redirect, session, request
from models import db

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET','POST', 'DELETE'])
def user():
    cities_query = '''SELECT city_name, ID_city FROM Topology;'''
    cities = db.executeQuery(cities_query)
           
    if "username" in session:
        if request.method == "GET":
            return render_template("user/profile.html", cities=cities, username=session["username"])

        elif request.method == "POST":
            city = request.form["city"]
            ID_area_query = f''' SELECT Topology.ID_area 
                                    FROM Topology
                                    WHERE ID_city = {city}
                                '''
            ID_area = db.executeQuery(ID_area_query)
            #uploads into database
            nusername= request.form[""]

            return render_template("user/profile.html")
    else:
        return redirect("/auth/login")