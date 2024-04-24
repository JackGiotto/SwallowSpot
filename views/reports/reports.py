from flask import Blueprint, render_template, request, session, redirect, url_for

reports_bp = Blueprint('reports', __name__, template_folder='templates')

@reports_bp.route('/reports/hydro/')
def hydro():
    return render_template("reports/hydro.html")

@reports_bp.route('/reports/snow/')
def snow():
    return render_template("reports/snow.html")

@reports_bp.route('/reports/ava/')
def ava():
    return render_template("reports/ava.html")

@reports_bp.route('/reports/')
def reports():
    return redirect(url_for("hydro"))