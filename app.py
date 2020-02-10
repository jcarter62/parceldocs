from flask import Flask, render_template, jsonify, request, make_response, redirect, send_file, send_from_directory
from flask_bootstrap import Bootstrap
from data import Parcels
from docs import ParcelFolder, FileList
from appsettings import Settings
import base64
from api.api_routes import api_routes
from fileio.file_routes import file_routes
from appsettings.appsetting_routes import appsetting_routes


app = Flask(__name__)
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(file_routes, url_prefix='/fileio')
app.register_blueprint(appsetting_routes, url_prefix='/settings')

Bootstrap(app)

#
# Utility methods
#
def float2datetime(epoc):
    import datetime
    result = ''
    dt = datetime.datetime.fromtimestamp(epoc)
    result = dt.strftime('%m/%d/%Y %H:%M:%S')
    return result


def b2k(num):
    result = '0k'
    n = int(num)
    k = round(n/1024, 2)
    result = str(k) + 'k'
    return result

#
# Routes
#
@app.route('/')
def home():
    context = {
        'title': 'home',
        'showsearch': True,
    }
    return render_template('home.html', context=context)


@app.route('/selected/<parcel_id>')
def route_selected_parcel(parcel_id):
    file_list = FileList(parcel=parcel_id)
    for f in file_list.files:
        fpath = bytes(f['fullpath'], 'utf-8')
        f['encoded'] = ''
        f['encoded'] = base64.standard_b64encode(fpath).decode('utf-8')
        f['mtime'] = float2datetime(f['info'].st_mtime)
        f['filesize'] = b2k(f['info'].st_size)

    p = Parcels()
    p.load_one_parcel(parcel_id)
    details = p.parcel

    context = {
        'title': 'parcel selected',
        'showsearch': False,
        'parcel': parcel_id,
        'files': file_list.files,
        'details': details
    }
    return render_template('selected_parcel.html', context=context)


@app.route('/parcels/<page>')
def route_parcels_page(page):
    pagenum = int(page)
    p = Parcels(page=pagenum).parcels
    context = {
        'title': 'parcels page %s' % str(page),
        'parcels': p,
        'page': page
    }
    return render_template('home.html', context=context)


@app.route('/favicon.ico')
def favicon():
    import os
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


if __name__ == '__main__':
    app.run()
