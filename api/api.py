from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/')
def test():
    return {
        'hello': 'there!'
    }