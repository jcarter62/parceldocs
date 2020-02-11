from flask import Blueprint, send_file
import os

wkroute = Blueprint('wkroute', __name__, static_folder='static', template_folder='templates')


@wkroute.route('/acme-challenge/<filename>')
def route_wk_sendfile(filename):
    print(filename)
    folder = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(folder, filename)
    return send_file(full_path)
