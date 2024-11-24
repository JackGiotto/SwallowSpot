from flask import session, request
from itsdangerous import URLSafeTimedSerializer
from models import db
import os

serializer = URLSafeTimedSerializer(os.getenv("SECRET"))

LONGER_SESSION_DURATION = 30 # days

def check_permanent_session() -> int:
    if "swsp_remember" in request.cookies:
        try:
            username = serializer.loads(request.cookies["swsp_remember"])
        except:
            return -1

        query = f"""SELECT username FROM User WHERE username = '{username}'"""
        if db.executeQuery(query):
            session["username"] = username
        else:
            return 1
        return 0
    else:
        return 1

def add_permanent_cookie(resp):
    if ("username" in session):
        signed_username = serializer.dumps(session["username"])
        resp.set_cookie("swsp_remember", signed_username, max_age=LONGER_SESSION_DURATION*24*60*60, httponly=True, secure=True)
        return resp
    else:
        return resp