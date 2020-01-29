from flask import Flask
from data import Parcels
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/test')
def route_load():
    p = Parcels()
    p.load_parcels()
    p.filter_parcels('011')
    return json.dumps(p.parcels_flt), 200


if __name__ == '__main__':
    app.run()
