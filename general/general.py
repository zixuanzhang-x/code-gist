from flask import Blueprint, render_template, redirect, redirect, url_for, session
from utils.login_util import login_required

route_blueprint = Blueprint('route_blueprint', __name__)

@route_blueprint.route('/')
def main_page():
    if 'profile' in session:
        return render_template('main.html', profile=session['profile'])
    return render_template('main.html')
