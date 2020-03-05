from flask import Blueprint, render_template, jsonify, redirect, request, g
import os

about_routes = Blueprint('about_routes', __name__, static_folder='static', template_folder='templates')


@about_routes.route('/application', methods=['GET'])
def route_setup():
    notes_file = os.path.abspath('notes.txt')
    txt_lines = []
    try:
        with open(notes_file, 'r') as f:
            while True:
                line = f.readline()
                if line <= '':
                    break
                txt_lines.append(line)
    except FileNotFoundError:
        pass

    context = {
        'title': 'About Application',
        'data': txt_lines,
        'auth': g.auth
    }

    return render_template('about.html', context=context)

