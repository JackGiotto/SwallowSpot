from flask import Flask, make_response, send_from_directory, url_for, render_template, abort, session, request, redirect
from flask_sslify import SSLify
from datetime import timedelta
from views import auth_bp, home_bp, profile_bp, reports_bp, info_bp
import os

app = Flask("Swallow Spot")
app.config["DEBUG"] = True
app.config["MAINTENANCE"] = False
sslify = SSLify(app)

app.permanent_session_lifetime = timedelta(minutes=50)
app.secret_key = "klosterpatia"
app.register_blueprint(auth_bp, url_prefix='/{}'.format(auth_bp.name))
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reports_bp, url_prefix='/{}'.format(reports_bp.name))
app.register_blueprint(info_bp)




@app.before_request
def check_under_maintenance():
    print(('superadmin' not in session and (request.path != '/profile/admin/' or request.path != '/end_maintenace')))
    if app.config["MAINTENANCE"] and not ('superadmin' in session and (request.path == '/profile/admin/' or request.path != '/end_maintenace')):
        return render_template('maintenance.html')

@app.route('/start_maintenance', methods=['POST'])
def start_maintenance():
    print("starting maintenance")
    app.config["MAINTENANCE"] = True
    print(app.config["MAINTENANCE"])
    return redirect(url_for("home.home")), 500

@app.route('/end_maintenance', methods=['POST'])
def end_maintenance():
    print("starting maintenance")
    app.config["MAINTENANCE"] = False
    return redirect(url_for("home.home")), 500

@app.route('/service_worker.js')
def sw():
    response=make_response(
                     send_from_directory("./static", "service_worker.js"))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    #ssl_context=('certificate/cert.pem', 'certificate/cert-key.pem')
    app.run(debug = True, host="0.0.0.0", port=os.getenv("PORT"))

