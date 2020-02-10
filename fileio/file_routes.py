from flask import Blueprint, render_template, jsonify, send_file, redirect, request
from werkzeug.utils import secure_filename
from docs import ParcelFolder
import os
import base64

file_routes = Blueprint('file_routes', __name__, static_folder='static', template_folder='templates')


@file_routes.route('/sendfile/<encoded>')
def route_sendfile(encoded):
    filename = base64.standard_b64decode(encoded).decode('ascii')
    print(filename)
    folder, file = os.path.split(filename)
    return send_file(filename, as_attachment=True, attachment_filename=file)


@file_routes.route('/deletefile/<encoded>/<parcel>')
def route_deletefile(encoded, parcel):
    filename = base64.standard_b64decode(encoded).decode('ascii')
    os.remove(filename)
    redirect_to = '/selected/%s' % parcel
    return redirect(redirect_to)


@file_routes.route('/renamefile/<encoded>/<parcel>')
def route_renamefile(encoded, parcel):
    filename = base64.standard_b64decode(encoded).decode('ascii')
    folder, file = os.path.split(filename)
    context = {
        'title': 'rename parcel file',
        'showsearch': False,
        'parcel': parcel,
        'file': file,
        'encoded': encoded
    }
    return render_template('rename_parcel_file.html', context=context)


@file_routes.route('/renamefile', methods=['POST'])
def route_renamefile_post():
    encoded = request.form['encoded']
    parcel = request.form['parcel']
    newfilename = request.form['newfilename']
    #
    # Extract full path, and then split into path and name.
    fullpath = base64.standard_b64decode(encoded).decode('ascii')
    folder, file = os.path.split(fullpath)
    #
    # create new full path
    newfullpath = os.path.join(folder, newfilename)
    #
    # now rename the old file to new file.
    os.rename(fullpath, newfullpath)

    redirect_to = '/selected/%s' % parcel
    return redirect(redirect_to)


@file_routes.route('/uploadfiles', methods=['POST'])
def route_uploadfiles():
    for item in request.files:
        f = request.files[item]
        parcel_id = request.form['parcel_id']
        pf = ParcelFolder(parcel=parcel_id)
        fullpath = os.path.join(pf.path, secure_filename(f.filename))
        f.save(fullpath)

    return jsonify({'status': 'ok'}), 200

