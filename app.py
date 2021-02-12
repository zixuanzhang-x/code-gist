from flask import Flask

from api.api import api

from db import db

app = Flask(__name__)

# Database setup
@app.before_first_request
def initialize():
    db.setup()

# Register Blueprints
app.register_blueprint(api, url_prefix='/api')