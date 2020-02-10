from flask import Flask, send_from_directory
from flask_bootstrap import Bootstrap
from api.api_routes import api_routes
from fileio.file_routes import file_routes
from appsettings.appsetting_routes import appsetting_routes
from ui.ui_routes import ui_routes
import os

app = Flask(__name__)
app.register_blueprint(ui_routes, url_prefix='')
app.register_blueprint(api_routes, url_prefix='/api')
app.register_blueprint(file_routes, url_prefix='/fileio')
app.register_blueprint(appsetting_routes, url_prefix='/settings')
Bootstrap(app)


@ui_routes.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == '__main__':
    app.run()
