import os
import requests

from flask import Blueprint, render_template, redirect, url_for, session, current_app

from urllib.parse import urlencode
from db import db
from auth.auth0 import auth0
from utils.login_util import login_required

route_blueprint = Blueprint('route_blueprint', __name__)

API_URI = os.environ["API_URI"]

@route_blueprint.route('/create')
@login_required
def create_page():
    return render_template('gist_page/create.html')

@route_blueprint.route('/')
def discover_page():
    if 'profile' in session:
        return render_template('gist_page/discover.html', profile=session['profile'])
    return render_template('gist_page/discover.html')

@route_blueprint.route('/user/<int:user_id>')
def user_page(user_id):
    users = requests.get(url = API_URI + '/api/user/' + str(user_id)).json()
    gists = requests.get(url = API_URI + '/api/user/' + str(user_id) + '/gist').json()
    starred = requests.get(url = API_URI + '/api/user/' + str(user_id) + '/star').json()

    return render_template('gist_page/user.html', user=users[0], gists=gists, starred=starred)

@route_blueprint.route('/gist/<int:gist_id>')
def gist_page(gist_id):
    gists = requests.get(url = API_URI + '/api/gist/' + str(gist_id)).json()
    comments = requests.get(url = API_URI + '/api/gist/' + str(gist_id) + '/comment').json()
    for idx in range(len(comments)):
        users = requests.get(url = API_URI + '/api/user/' + str(comments[idx]['user_id'])).json()
        comments[idx]['user_name'] = users[0]['user_name']
        comments[idx]['picture'] = users[0]['picture']

    if 'profile' in session:
        auth0_id = session['profile']['user_id']
        return render_template('gist_page/gist.html', gist=gists[0], comments = comments, auth0_id=auth0_id)
    else:
        return render_template('gist_page/gist.html', gist=gists[0], comments = comments)

@route_blueprint.route('/gist/<int:gist_id>/stargazers')
def gist_stargazers_page(gist_id):
    gists = requests.get(url = API_URI + '/api/gist/' + str(gist_id)).json()
    stargazers = requests.get(url = API_URI + '/api/gist/' + str(gist_id) + '/star').json()

    return render_template('gist_page/gist_stargazers.html', gist=gists[0], stargazers=stargazers)

@route_blueprint.route('/login')
def user_login():
    if 'profile' in session:
        return redirect(url_for('route_blueprint.discover_page'))
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

    requests.post(API_URI + '/api/user', \
        data={'auth0_id': userinfo['sub'],
              'user_name': userinfo['name'],
              'picture': userinfo['picture'],
              })

    return redirect(url_for('route_blueprint.create_page'))

@route_blueprint.route('/logout')
def user_logout():
    session.clear()
    params = { 'returnTo': url_for('route_blueprint.discover_page', _external=True), 'client_id': os.environ['AUTH0_CLIENT_ID'] }
    return redirect(auth0().api_base_url + '/v2/logout?' + urlencode(params))
