import os

from flask import Blueprint, render_template, redirect, url_for, session
from utils.login_util import login_required

from urllib.parse import urlencode
from db import db
from auth.auth0 import auth0

route_blueprint = Blueprint('route_blueprint', __name__)

@route_blueprint.route('/')
def main_page():
    if 'profile' in session:
        return render_template('main.html', profile=session['profile'])
    return render_template('main.html')

@route_blueprint.route('/login')
def user_login():
    if 'profile' in session:
        return redirect(url_for('route_blueprint.main_page'))
    else:
        return auth0().authorize_redirect(redirect_uri=url_for('route_blueprint.callback', _external=True))

@route_blueprint.route('/callback')
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
    # TODO: insert to user in db

    return redirect(url_for('route_blueprint.main_page'))

@route_blueprint.route('/logout')
@login_required
def user_logout():
    session.clear()
    params = { 'returnTo': url_for('route_blueprint.main_page', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID'] }
    return redirect(auth0().api_base_url + '/v2/logout?' + urlencode(params))
