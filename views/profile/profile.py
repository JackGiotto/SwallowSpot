from flask import Blueprint, render_template, redirect, session, request
from models import db

profile_bp = Blueprint('profile', __name__, template_folder='templates')

@profile_bp.route('/profile/', methods=['GET','POST', 'DELETE'])
def user():
    cities_query = '''SELECT city_name, ID_city FROM Topology;'''
    cities = db.executeQuery(cities_query)

    if "username" in session:
        id_user = db.executeQuery("SELECT ID_user FROM User WHERE username ='"+session["username"]+"';")
        id_user = id_user[0]["ID_user"]
        if request.method == "GET":
            return render_template("user/profile.html", cities=cities, username=session["username"])

        elif request.method == "POST":
            if "new_username" in request.form:
                new_username = request.form["new_username"]
                db.executeQuery("UPDATE User SET username = '"+str(new_username)+"' WHERE ID_user = '"+str(id_user)+"';")
                session["username"]=new_username
                return render_template("user/profile.html", cities=cities, username=session["username"])

            elif "city" in request.form:
                new_zone = request.form["city"]#a quanto pare viene restituito l'id ma non ho voglia di capire perché... buonanotte... oh no buongiorno tini
                update= "UPDATE User SET ID_area = '"+str(new_zone)+"' WHERE ID_user = "+str(id_user)+";"
                db.executeQuery(update)

            elif "psw_change" in request.form:#questo lo faccio domani chill
                new_password = request.form["new_password"]

            return render_template("user/profile.html")
        elif request.method== "DELETE":
            pass
    else:
        return redirect("/auth/login")




        #city = request.form["city"]
            #ID_area_query = f''' SELECT Topology.ID_area 
            #                        FROM Topology
             #                       WHERE ID_city = {city}
            #                    '''
            #ID_area = db.executeQuery(ID_area_query)
            #uploads into database
            