from flask import Flask, send_from_directory, session, request, json, make_response, url_for, redirect, g
from flask_bootstrap import Bootstrap
from flask_mongo_session.session_processor import MongoSessionProcessor
from api.api_routes import api_routes
from fileio.file_routes import file_routes
from appsettings.appsetting_routes import appsetting_routes
from ui.ui_routes import ui_routes
from wkroute.wkroute import wkroute
from auth.auth_routes import auth_routes
# from auth.auth_routes import logged_in
from auth.auth_routes import UserInfo
import uuid

import os

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
    app.session_cookie_name = s_cookie
    app.session_interface = MongoSessionProcessor(_connection_)
except Exception as e:
    print('Error with Settings... %s ' % e.__str__())


@app.before_request
def app_before_request():
    auth = {
        'authenticated': False,
        'user': False,
        'admin': False
    }
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
    g.auth = auth


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == '__main__':
    app.run()
