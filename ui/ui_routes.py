from flask import Blueprint, render_template, send_from_directory, session
from docs import FileList
from data import Parcels
import base64
import os

ui_routes = Blueprint('ui_routes', __name__, static_folder='static', template_folder='templates')


@ui_routes.route('/')
def home():
    context = {
        'title': 'home',
        'showsearch': True,
    }
    session['page'] = '/'
    return render_template('home.html', context=context)


@ui_routes.route('/selected/<parcel_id>')
def route_selected_parcel(parcel_id):
    def float2datetime(epoc):
        import datetime
        result = ''
        dt = datetime.datetime.fromtimestamp(epoc)
        result = dt.strftime('%m/%d/%Y %H:%M:%S')
        return result

    def b2k(num):
        result = '0k'
        n = int(num)
        k = round(n / 1024, 2)
        result = str(k) + 'k'
        return result

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
    session['page'] = '/selected/%s' % parcel_id
    return render_template('selected_parcel.html', context=context)


@ui_routes.route('/parcels/<page>')
def route_parcels_page(page):
    pagenum = int(page)
    p = Parcels(page=pagenum).parcels
    context = {
        'title': 'parcels page %s' % str(page),
        'parcels': p,
        'page': page
    }
    return render_template('home.html', context=context)


