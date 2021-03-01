from flask import Blueprint, request, current_app, jsonify, make_response
from db import db
from utils.api_util import extract_gists_from_cursor, extract_users_from_cursor

user_api_blueprint = Blueprint('user_api_blueprint', __name__)


@user_api_blueprint.route('/user', methods=['POST'])
def get_or_create_user():
    """
    Create a new user with provided auth0 id.
    (do nothing if user already exits)
    Return user's PostgreSQL id.
    """
    auth0_id = request.form.get('auth0_id')
    with db.get_db_cursor(True) as cursor:
        cursor.execute(
            "SELECT user_id from gist_user WHERE auth0_id = %s;", (auth0_id,))

        if cursor.rowcount == 1:  # user already exists
            user_id = cursor.fetchone()[0]
        else:  # user does not exists yet, create new user
            picture = request.form.get('picture')
            user_name = request.form.get('user_name')
            cursor.execute(
                "INSERT INTO gist_user(auth0_id, user_name, picture) VALUES(%s, %s, %s) RETURNING user_id;", (auth0_id, user_name, picture))
            user_id = cursor.fetchone()[0]
            current_app.logger.info(
                f"Created new user: {{'user_id': {user_id}, 'user_name': {user_name}, 'auth0_id': {auth0_id}}}")

        return {'user_id': user_id}


@user_api_blueprint.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Return this user with the user_id."""
    with db.get_db_cursor(True) as cursor:
        cursor.execute(
            "SELECT * FROM gist_user WHERE user_id = %s", (user_id,))
        return jsonify(extract_users_from_cursor(cursor))


@user_api_blueprint.route('/user/<int:user_id>/star', methods=['GET'])
def get_user_stars(user_id):
    """Return a list of gists that this user starred."""
    with db.get_db_cursor(True) as cursor:
        cursor.execute("""SELECT gist.* FROM star
                          JOIN gist ON star.gist_id = gist.gist_id
                          WHERE star.user_id = %s;""", (user_id,))
        return jsonify(extract_gists_from_cursor(cursor))


@user_api_blueprint.route('/user/<int:user_id>/gist', methods=['GET'])
def get_user_gists(user_id):
    """Return a list of gists that belong to this user."""
    with db.get_db_cursor(True) as cursor:
        cursor.execute("SELECT * FROM gist WHERE user_id = %s;;", (user_id,))
        return jsonify(extract_gists_from_cursor(cursor))
