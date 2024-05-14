from flask import Flask, make_response, send_from_directory
from flask_sslify import SSLify, render_template
from datetime import timedelta
from views import auth_bp, home_bp, profile_bp, reports_bp, info_bp
import os

app = Flask("Swallow Spot")
app.config["DEBUG"] = True
sslify = SSLify(app)

app.permanent_session_lifetime = timedelta(minutes=50)
app.secret_key = "klosterpatia"
app.register_blueprint(auth_bp, url_prefix='/{}'.format(auth_bp.name))
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reports_bp, url_prefix='/{}'.format(reports_bp.name))
app.register_blueprint(info_bp)

@app.route('/service_worker.js')
def sw():
    response=make_response(
                     send_from_directory("./static", "service_worker.js"))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response@app.errorhandler(404)

def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=os.getenv("PORT"), ssl_context=('certificate/cert.pem', 'certificate/cert-key.pem'))

