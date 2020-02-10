from flask import Blueprint, render_template, jsonify
from data import Parcels
from docs import FileList

api_routes = Blueprint('api_routes', __name__, static_folder='static', template_folder='templates')

@api_routes.route('/parcels')
def route_api_parcels():
    p = Parcels()
    p.load_parcels()
    return jsonify(p.parcels), 200


@api_routes.route('/parcel/<parcel>')
def route_api_parcel_parcel(parcel):
    p = Parcels()
    p.load_one_parcel(parcel)
    if p.parcel is None:
        result_code = 204
    else:
        result_code = 200
    return jsonify(p.parcel), result_code


@api_routes.route('/parcel-doc-info/<parcel>')
def route_api_parcel_doc_info(parcel):
    files = FileList(parcel=parcel)
    files_details = files.file_sys_details()
    return jsonify(files_details), 200


@api_routes.route('/parcel-search/<srch_str>')
def route_parcel_search(srch_str):
    search_str = srch_str
    p = Parcels()
    p.filter_parcels(partial=search_str)
    return jsonify(p.parcels_flt), 200


@api_routes.route('/parcel-files/<parcel>')
def route_parcel_files(parcel):
    file_list = FileList(parcel=parcel)
    return jsonify(file_list.files), 200


