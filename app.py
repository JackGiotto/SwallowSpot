
# Read env file as first thing
import os
from dotenv import load_dotenv
from utils.wsgi_utils import read_env_file


if __name__ == "__main__":
    load_dotenv()
    start_path = "./"
else:
    start_path = "/var/www/swallowspot.it/SwallowSpot/"
    read_env_file(start_path + ".env")

from flask import Flask, render_template, session, request, make_response, redirect, url_for
from flask_cors import CORS
from flask_minify import minify
from datetime import timedelta
from views import auth_bp, home_bp, profile_bp, reports_bp, info_bp, feedbacks_bp, special_bp
from utils.cookies_utils import check_permanent_session, add_permanent_cookie



os.environ["start_path"] = start_path

app = Flask("Swallow Spot", template_folder=start_path + "templates")
app.config["DEBUG"] = True

app.permanent_session_lifetime = timedelta(minutes=50)
app.secret_key = os.getenv("SECRET")
app.register_blueprint(home_bp)
app.register_blueprint(special_bp)
app.register_blueprint(auth_bp, url_prefix='/{}'.format(auth_bp.name))
app.register_blueprint(profile_bp)
app.register_blueprint(reports_bp, url_prefix='/{}'.format(reports_bp.name))
app.register_blueprint(info_bp)
app.register_blueprint(feedbacks_bp)


minify(app=app, html=True, js=True, cssless=True)
CORS(app, supports_credentials=True)  # Enable CORS with credentials support

@app.before_request
def permanent_session_control():
    if "username" not in session:
        if "swsp_remember" in request.cookies:
            if check_permanent_session() == -1:
                resp = make_response(redirect(url_for("home.home")))
                resp.delete_cookie("swsp_remember")
                return resp

@app.before_request
def check_under_maintenance():
    if os.environ["MAINTENANCE"] == "True" and not ('superadmin' in session) and ('snake' not in request.path) and ('login' not in request.path):
        return render_template('maintenance.html')

@app.after_request
def add_cookie(response):
    if "swsp_remember" in request.cookies:
        return add_permanent_cookie(response)
    else:
        return response


@app.route('/start_maintenance', methods=['POST'])
def start_maintenance():
    if 'superadmin' in session:
        print("starting maintenance")
        os.environ["MAINTENANCE"] = "True"
        #print(app.config["MAINTENANCE"])
        return "started", 200

@app.route('/end_maintenance', methods=['POST'])
def end_maintenance():
    if 'superadmin' in session:
        print("ending maintenance")
        os.environ["MAINTENANCE"] = "False"
        return "ended", 200

@app.errorhandler(404)
def page_not_found(e):
    """when user insert in url bar an url that is not present
    """
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=os.getenv("PORT"))

