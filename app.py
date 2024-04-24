from flask import Flask
from datetime import timedelta
from views.auth import auth
from views.home import home

app = Flask(__name__)
app.config["DEBUG"] = True

app.permanent_session_lifetime = timedelta(minutes=5)
app.secret_key = "klosterpatia"
app.register_blueprint(auth)
app.register_blueprint(home)

if __name__ == "__main__":
    app.run(debug = True, host="0.0.0.0", port=11599)