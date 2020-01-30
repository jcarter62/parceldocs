from flask import Flask, render_template, jsonify, request, make_response
from flask_bootstrap import Bootstrap
from data import Parcels
import json

app = Flask(__name__)
Bootstrap(app)


@app.route('/')
def hello_world():
    context = {
        'title': 'home'
    }
    return render_template('home.html', context=context)


@app.route('/test')
def route_load():
    p = Parcels()
    p.load_parcels()
    p.filter_parcels('011')
    return json.dumps(p.parcels_flt), 200


@app.route('/api/parcels')
def route_api_parcels():
    p = Parcels()
    p.load_parcels()
    return jsonify(p.parcels), 200


if __name__ == '__main__':
    app.run()
