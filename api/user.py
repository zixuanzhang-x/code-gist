from db import db
import os

from flask import Blueprint, render_template, redirect, url_for, session
from urllib.parse import urlencode
from datetime import datetime

from auth.auth import auth0

user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.route('/login')
def user_login():
    if 'profile' in session:
        return redirect(url_for('route_blueprint.main_page'))
    else:
        return auth0().authorize_redirect(redirect_uri=url_for('user_blueprint.user_register', _external=True))

@user_blueprint.route('/register')
def user_register():
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
    # insert to user in db
    with db.get_db_cursor(True) as cur:
        cur.execute("INSERT INTO user (username, avatar, signed_up) \
            values (%s, %s)", (userinfo['name'], userinfo['picture'], datetime.now())
        )

    return redirect(url_for('route_blueprint.main_page'))

@user_blueprint.route('/logout')
def user_logout():
    session.clear()
    params = { 'returnTo': url_for('route_blueprint.main_page', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID'] }
    return redirect(auth0().api_base_url + '/v2/logout?' + urlencode(params))
