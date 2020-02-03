from flask import Flask, render_template, jsonify, request, make_response, redirect
from flask_bootstrap import Bootstrap
from data import Parcels
import json

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def hello_world():
    p = Parcels().parcels

    context = {
        'title': 'home',
        'parcels': p
    }
    return render_template('home.html', context=context)


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


@app.route('/setup', methods=['GET', 'POST'])
def route_setup():
    from appsettings import Settings
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


if __name__ == '__main__':
    app.run()
