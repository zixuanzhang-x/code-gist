import os
import requests

from flask import Blueprint, redirect, session, url_for
from functools import wraps
from urllib.parse import urlencode

from auth.auth0 import auth0

auth_blueprint = Blueprint('auth_blueprint', __name__)

API_URI = os.environ["API_URI"]

@auth_blueprint.route('/login')
def user_login():
    if 'profile' in session:
        return redirect(url_for('route_blueprint.discover_page'))
    else:
        return auth0().authorize_redirect(redirect_uri=url_for('auth_blueprint.callback', _external=True))

@auth_blueprint.route('/callback')
def callback():
    # register by auth0
    auth0().authorize_access_token()
    response = auth0().get('userinfo')
    userinfo = response.json()

    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    requests.post(API_URI + '/api/user', \
        data={'auth0_id': userinfo['sub'],
              'user_name': userinfo['name'],
              'picture': userinfo['picture'],
              })

    return redirect(url_for('route_blueprint.create_page'))

@auth_blueprint.route('/logout')
def user_logout():
    session.clear()
    params = { 'returnTo': url_for('route_blueprint.discover_page', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID'] }
    return redirect(auth0().api_base_url + '/v2/logout?' + urlencode(params))

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for('auth_blueprint.user_login'))
        return f(*args, **kwargs)
    return decorated
