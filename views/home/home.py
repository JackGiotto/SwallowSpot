from flask import Blueprint, render_template
import requests

home_page = Blueprint('home', __name__, template_folder = 'templates')


@home_page.route('/')
def home():
    return render_template("home.html", app=applicationName)