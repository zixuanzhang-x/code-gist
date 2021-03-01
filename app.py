import os

from flask import Flask

from api.user_api import user_api_blueprint
from api.gist_api import gist_api_blueprint
from utils.error_page_util import error_blueprint
from general.general import route_blueprint

from db import db
from auth.auth0 import auth0_setup

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

# Database and auth0 setup
@app.before_first_request
def initialize():
    db.setup()
    auth0_setup()

# Register API Blueprints
app.register_blueprint(user_api_blueprint, url_prefix='/api/')
app.register_blueprint(gist_api_blueprint, url_prefix='/api/')

# Register Router Blueprints
app.register_blueprint(route_blueprint)
app.register_blueprint(error_blueprint)
