import os

from flask import Flask

from api.api import api
from utils.error_page_util import error_blueprint
from api.user import user_blueprint
from general.general import route_blueprint

from db import db
from auth.auth import auth0_setup

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

# Database and auth0 setup
@app.before_first_request
def initialize():
    db.setup()
    auth0_setup()

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(user_blueprint)
app.register_blueprint(route_blueprint)
app.register_blueprint(error_blueprint)
