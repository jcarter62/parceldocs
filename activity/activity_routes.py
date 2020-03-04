from flask import Blueprint, render_template, jsonify, redirect, request, g
from appsettings import Settings
from useractivity import UserActivity


activity_routes = Blueprint('activity_routes', __name__, static_folder='static', template_folder='templates')


@activity_routes.route('/log', methods=['GET'])
def route_setup():
    if g.auth['admin']:
        settings = Settings()
        ua = UserActivity()
        activity_log = ua.list_all_activity()
        context = {
            'log': activity_log,
            'auth': g.auth
        }
        return render_template('log.html', context=context)
    else:
        return redirect('/')
