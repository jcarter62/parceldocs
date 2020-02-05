from flask import Flask, render_template, jsonify, request, make_response, redirect, send_file, send_from_directory
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from data import Parcels
from docs import ParcelFolder, FileList
import json
from appsettings import Settings
from docs import ParcelFolder
import os
import base64

app = Flask(__name__)
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
    import datetime
    file_list = FileList(parcel=parcel_id)
    for f in file_list.files:
        fpath = bytes(f['fullpath'], 'utf-8')
        f['encoded'] = ''
        f['encoded'] = base64.standard_b64encode(fpath).decode('utf-8')
        f['mtime'] = float2datetime(f['info'].st_mtime)
        f['filesize'] = b2k(f['info'].st_size)

    context = {
        'title': 'parcel selected',
        'showsearch': False,
        'parcel': parcel_id,
        'files': file_list.files
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


@app.route('/api/parcels')
def route_api_parcels():
    p = Parcels()
    p.load_parcels()
    return jsonify(p.parcels), 200


@app.route('/api/parcel-search/<srch_str>')
def route_parcel_search(srch_str):
    search_str = srch_str
    p = Parcels()
    p.filter_parcels(partial=search_str)
    return jsonify(p.parcels_flt), 200


@app.route('/api/parcel-files/<parcel>')
def route_parcel_files(parcel):
    file_list = FileList(parcel=parcel)
    return jsonify(file_list.files), 200


@app.route('/setup', methods=['GET', 'POST'])
def route_setup():
    if request.method == 'GET':
        settings = Settings()
        context = {'settings': settings.items}
        return render_template('setup.html', context=context)
    else:
        # Extract each item from form, and save back to settings.
        settings = Settings()
        for item in settings.items:
            formitem = request.form[item['name']]
            item['value'] = formitem
        settings.save_config()
        return redirect('/setup')


@app.route('/sendfile/<encoded>')
def route_sendfile(encoded):
    filename = base64.standard_b64decode(encoded).decode('ascii')
    print(filename)
    folder, file = os.path.split(filename)
    return send_file(filename, as_attachment=True, attachment_filename=file)


@app.route('/deletefile/<encoded>/<parcel>')
def route_deletefile(encoded, parcel):
    filename = base64.standard_b64decode(encoded).decode('ascii')
    os.remove(filename)
    redirect_to = '/selected/%s' % parcel
    return redirect(redirect_to)


@app.route('/uploadfile', methods=['POST'])
def route_uploadfile():
    if request.method == 'POST':
        f = request.files['file']
        parcel_id = request.form['parcel_id']
        pf = ParcelFolder(parcel=parcel_id)
        fullpath = os.path.join(pf.path, secure_filename(f.filename))
        f.save(fullpath)

        redirect_to = '/selected/%s' % parcel_id
        return redirect(redirect_to)


@app.route('/favicon.ico')
def favicon():
    import os
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


if __name__ == '__main__':
    app.run()
