from flask import Blueprint, make_response, send_from_directory
import os

special_bp = Blueprint('special', __name__, template_folder='templates')

@special_bp.route('/service_worker.js')
def sw():
    response = make_response(
                     send_from_directory(os.environ["start_path"] + "static", "service_worker.js"))
    #change the content header file. Can also omit; flask will handle correctly.
    response.headers['Content-Type'] = 'application/javascript'
    return response

@special_bp.route('/robots.txt')
def robots():
    response = make_response(
                     send_from_directory(os.environ["start_path"] + "static", "robots.txt"))
    response.headers['Content-Type'] = 'text/plain'
    return response

@special_bp.route('/sitemap.xml')
def sitemap():
    response = make_response(
                     send_from_directory(os.environ["start_path"] + "static", "sitemap.xml"))
    response.headers['Content-Type'] = 'application/xml'
    return response
