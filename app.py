from flask import Flask, send_from_directory, session, request, json, make_response, url_for, redirect, g
from flask_bootstrap import Bootstrap
from flask_mongo_session.session_processor import MongoSessionProcessor
from api.api_routes import api_routes
from fileio.file_routes import file_routes
from appsettings.appsetting_routes import appsetting_routes
from ui.ui_routes import ui_routes
from wkroute.wkroute import wkroute
from auth.auth_routes import auth_routes
from auth.auth_routes import UserInfo
from pymongo import MongoClient
from waitress import serve
import logging
import os
import datetime


app = Flask(__name__)
app.register_blueprint(ui_routes, url_prefix='')
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(file_routes, url_prefix='/fileio')
app.register_blueprint(appsetting_routes, url_prefix='/settings')
app.register_blueprint(wkroute, url_prefix='/.well-known')
app.register_blueprint(auth_routes, url_prefix='/auth')

Bootstrap(app)

#
# Setup Server based session storage.
#
try:
    from appsettings import Settings
    settings = Settings()
    s_host = settings.get('mongo_host')
    s_port = settings.get('mongo_port')
    s_db = settings.get('mongo_db')
    s_cookie = settings.get('session_cookie')
    _connection_ = 'mongodb://%s:%s/%s' % (s_host, s_port, s_db)

    _client_ = MongoClient(host=['%s:%s' % (s_host, s_port)], serverSelectionTimeoutMS= 2000)
    _client_status_ = _client_.server_info()
    del _client_
    del _client_status_

    app.session_cookie_name = s_cookie
    app.session_interface = MongoSessionProcessor(_connection_)
except Exception as e:
    print('Error with Settings... %s ' % e.__str__())

@app.before_request
def app_before_request():

    log_request(req=request)

    auth = {
        'authenticated': False,
        'user': False,
        'admin': False,
        'name': ''
    }
    #
    try:
        auth['name'] = session['user']['name']
    except Exception as e:
        auth['name'] = str(e)

    g.auth = auth
    #
    # Don't check if we are logged in for the following paths
    #
    try:
        path = request.full_path + '    '
        shortpath = path[0:4]
        if shortpath in ['/api', '/fil', '/set', '/.we', '/aut']:
            return
    finally:
        pass

    user = UserInfo(sess=session)

    if user.authenticated:
        auth['authenticated'] = True
        if user.is_user:
            auth['user'] = True
        if user.is_admin:
            auth['admin'] = True

        # Record user name if possible.

    g.auth = auth


@app.after_request
def after_request_func(response):
    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')


def log_request(req: request = None):
    if req == None:
        return

    msg = '%s - %s ' % (datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), req.url)
    print(msg)
    return


if __name__ == '__main__':
    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)
    serve(app, host='0.0.0.0', port=5000)
