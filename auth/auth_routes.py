import msal as msal
from flask import Blueprint, render_template, session, redirect, url_for, request
import uuid
from appsettings import Settings
from .sessiondestroy import SessionDestroy


auth_routes = Blueprint('auth_routes', __name__, static_folder='static', template_folder='templates')


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
    return render_template('login.html', auth_url=auth_url, version=msal.__version__)


@auth_routes.route(Settings().get('ms-redirect_path'))
def auth_authorized():
    if request.args.get('state') != session.get('state'):
        return redirect(url_for('index'))
    if 'error' in request.args:
        return render_template('auth_error.html', result=request.args)
    if request.args.get('code'):
        cache = _load_cache()
        result = _build_msal_app(cache=cache).acquire_token_by_authorization_code(
            request.args['code'],
            scopes=Settings().get('ms-scope'),
            redirect_uri=url_for('authorized', _external=True))
        if 'error' in result:
            return render_template('auth_error.html', result=result)
        session['user'] = result.get('id_token_claims')
        _save_cache(cache)
    return redirect(url_for('index'))


@auth_routes.route('/logout')
def auth_logout():
    SessionDestroy(sess=session, req=request)

    redirect_path = Settings().get('ms-authority') + "/oauth2/v2.0/logout" + "?post_logout_redirect_uri=" + url_for('index', _external=True)
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
        client_credential=settings.get('ms-client_secret'), token_cache=cache)


def _build_auth_url(authority=None, scopes=None, state=None):
    return _build_msal_app(authority=authority).get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for("authorized", _external=True))


def _get_token_from_cache(scope=None):
    cache = _load_cache()  # This web app maintains one cache per session
    cca = _build_msal_app(cache=cache)
    accounts = cca.get_accounts()
    if accounts:  # So all account(s) belong to the current signed-in user
        result = cca.acquire_token_silent(scope, account=accounts[0])
        _save_cache(cache)
        return result


