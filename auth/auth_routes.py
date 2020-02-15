import msal as msal
from flask import Blueprint, render_template, session, redirect, url_for, request
import uuid
from appsettings import Settings
from .sessiondestroy import SessionDestroy
import requests, json
from ui.ui_routes import ui_routes


auth_routes = Blueprint('auth_routes', __name__, static_folder='static', template_folder='templates')


class UserInfo:

    def __init__(self, sess: session ):
        self.session = sess
        self.authenticated = False
        self.is_user = False
        self.is_admin = False
        try:
            self.email = self.session.get('user')['preferred_username'].lower()
            self.name = self.session.get('user')['name'].lower()
        except Exception as e:
            self.email = ''
            self.name = ''

        self.logged_in()
        if self.authenticated:
            self.load_userinfo()


    def logged_in(self):
        if self.session.get('user'):
            self.authenticated = True
        else:
            self.authenticated = False
        return

    #
    # Determine user type
    #
    def load_userinfo(self):
        #
        # obtain /.../api/users, find
        #
        settings = Settings()
        url = settings.get('ad_api') + '/api/userinfo'
        formdata = {'key': settings.get('ad_api_key'), 'identity': self.name}
        try:
            data = requests.post(url, data=formdata)
            if data.status_code != 200:
                return
            record = data.json()

            if record['name'] == self.name:
                self.authenticated = True
                self.is_admin = record['admin']
                self.is_user = record['user']
            else:
                self.authenticated = False
                self.is_user = False
                self.is_admin = False

        except Exception as e:
            print('Error in check_groups: %s' % e.__str__())

        return


def logged_in(sess: session) -> bool:
    if not sess.get('user'):
        result = False
    else:
        result = True
    return result


@auth_routes.route('/login')
def auth_route():
    settings = Settings()
    guid = str(uuid.uuid4())
    session['state'] = guid
    auth_url = _build_auth_url(scopes=settings.get('ms-scope'), state=session['state'])
    return redirect(auth_url)
#    return render_template('login.html', auth_url=auth_url, version=msal.__version__)


@auth_routes.route(Settings().get('ms-redirect_path'))
def auth_authorized():
    if request.args.get('state') != session.get('state'):
        return redirect(url_for('ui_routes.home'))
    if 'error' in request.args:
        return render_template('auth_error.html', result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        code = request.args['code']
        scopes = [Settings().get('ms-scope')]
        uri = url_for('auth_routes.auth_authorized', _external=True)

        result = _build_msal_app(cache=cache)\
            .acquire_token_by_authorization_code(code, scopes=scopes, redirect_uri=uri)
        if 'error' in result:
            return render_template('auth_error.html', result=result)
        session['user'] = result.get('id_token_claims')
        _save_cache(cache)
    return redirect(url_for('ui_routes.home'))


@auth_routes.route('/logout')
def auth_logout():
    SessionDestroy(sess=session, req=request)
    redirect_path = Settings().get('ms-authority') + "/oauth2/v2.0/logout" + "?post_logout_redirect_uri=" + url_for('ui_routes.home', _external=True)
    response = redirect(redirect_path)
    response.delete_cookie(Settings().get('session_cookie'))
    return response


def _load_cache():
    cache = msal.SerializableTokenCache()
    if session.get("token_cache"):
        cache.deserialize(session["token_cache"])
    return cache


def _save_cache(cache):
    if cache.has_state_changed:
        session["token_cache"] = cache.serialize()


def _build_msal_app(cache=None, authority=None):
    settings = Settings()
    return msal.ConfidentialClientApplication(
        settings.get('ms-client_id'), authority=authority or settings.get('ms-authority'),
        client_credential=settings.get('ms-client_secret'), token_cache=cache, validate_authority=False)


def _build_auth_url(authority=None, scopes=None, state=None):
    p1 = ([scopes] or [])
    p2 = state or str(uuid.uuid4())
    p3 = url_for('auth_routes.auth_authorized', _external=True)
    return _build_msal_app(authority=authority).get_authorization_request_url(
        p1, state=p2, redirect_uri=p3)


def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


