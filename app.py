from flask import Flask
from datetime import timedelta
from views import auth_bp, home_bp, profile_bp, reports_bp

app = Flask("Swallow Spot")
app.config["DEBUG"] = True

app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "klosterpatia"
app.register_blueprint(auth_bp, url_prefix='/{}'.format(auth_bp.name))
app.register_blueprint(home_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(reports_bp)

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=11599)