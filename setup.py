from flask import Flask, redirect, render_template, request, g
from appsettings.appsetting_routes import appsetting_routes
from flask_bootstrap import Bootstrap
from appsettings import Settings


app = Flask(__name__)
app.register_blueprint(appsetting_routes, url_prefix='/settings')
Bootstrap(app)


@app.before_request
def app_before_request():
    auth = {'authenticated': False, 'user': False, 'admin': False, 'name': ''}
    #
    g.auth = auth

@app.after_request
def after_request_func(response):
    return response


@app.route('/')
def hello_world():
    return redirect('/settings/setup')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
