from flask import Flask, make_response, send_from_directory, url_for, render_template, abort, session, request, redirect
from flask_cors import CORS
from flask_sslify import SSLify
from datetime import timedelta
from views import auth_bp, home_bp, profile_bp, reports_bp, info_bp
from dotenv import load_dotenv
from utils.wsgi_utils import read_env_file
import os


if __name__ == "__main__":
    load_dotenv()
    start_path = "./"
else:
    start_path = "/var/www/swallowspot.it/SwallowSpot/"
    read_env_file(start_path + ".env")

os.environ["start_path"] = start_path

app = Flask("Swallow Spot", template_folder=start_path + "templates")
app.config["DEBUG"] = False
app.config["MAINTENANCE"] = (os.getenv("MAINTENANCE") == "True")

if __name__ == "__main__":
    sslify = SSLify(app)



app.permanent_session_lifetime = timedelta(minutes=50)
app.secret_key = "klosterpatia"
app.register_blueprint(auth_bp, url_prefix='/{}'.format(auth_bp.name))
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reports_bp, url_prefix='/{}'.format(reports_bp.name))
app.register_blueprint(info_bp)


CORS(app, supports_credentials=True)  # Enable CORS with credentials support

@app.before_request
def check_under_maintenance():
    if app.config["MAINTENANCE"] and not ('superadmin' in session) and ('snake' not in request.path) and ('login' not in request.path):
        return render_template('maintenance.html')

@app.route('/start_maintenance', methods=['POST'])
def start_maintenance():
    print("starting maintenance")
    app.config["MAINTENANCE"] = True
    print(app.config["MAINTENANCE"])
    return "started", 200

@app.route('/end_maintenance', methods=['POST'])
def end_maintenance():
    print("starting maintenance")
    app.config["MAINTENANCE"] = False
    return "ended", 200

@app.route('/service_worker.js')
def sw():
    response=make_response(
                     send_from_directory("./static", "service_worker.js"))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.errorhandler(404)
def page_not_found(e):
    """when user insert in url bar an url that is not present
    """
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug = True, host="127.0.0.1", port=os.getenv("PORT"))

