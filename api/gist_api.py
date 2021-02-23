from flask import Blueprint, request, current_app, jsonify
from db import db
from utils.api_util import extract_gists_from_cursor, extract_comments_from_cursor, extract_users_from_cursor

gist_api_blueprint = Blueprint('gist_api_blueprint', __name__)


@gist_api_blueprint.route('/gist', methods=['GET'])
def get_gists():
    q = request.args.get('q', None)
    with db.get_db_cursor(True) as cursor:
        if q:  # search for gists match pattern q
            cursor.execute(
                "SELECT * FROM gist WHERE gist_name LIKE %s", (f'%{q}%',))
        else:
            cursor.execute("SELECT * FROM gist;")
        return jsonify(extract_gists_from_cursor(cursor))


@gist_api_blueprint.route('/gist', methods=['POST'])
def create_gists():
    user_id = request.form.get('user_id')
    gist_name = request.form.get('gist_name')
    user_name = request.form.get('user_name')
    description = request.form.get('description')
    content = request.form.get('content')
    is_forked = request.form.get('is_forked', False)
    forked_from = request.form.get('forked_from', None)
    with db.get_db_cursor(True) as cursor:
        cursor.execute(
            """INSERT INTO gist(user_id,
                                gist_name,
                                user_name, 
                                description,
                                content, 
                                created,
                                last_modified,
                                is_forked,
                                forked_from)
               VALUES (%s, %s, %s, %s, %s, current_timestamp, current_timestamp, %s, %s)
               RETURNING user_id;""",
            (user_id, gist_name, user_name, description, content, is_forked, forked_from))
        gist_id = cursor.fetchone()[0]
        current_app.logger.info(
            f"Created new gist: {{'gist_id': {gist_id}, 'user_id': {user_id}}}")

        return {'gist_id': gist_id}


@gist_api_blueprint.route('/gist/<int:gist_id>', methods=['GET'])
def get_gist(gist_id):
    with db.get_db_cursor(True) as cursor:
        cursor.execute("SELECT * FROM gist WHERE gist_id = %s;;", (gist_id,))
        return jsonify(extract_gists_from_cursor(cursor))


@gist_api_blueprint.route('/gist/<int:gist_id>', methods=['PUT'])
def update_gist(gist_id):
    return {}


@gist_api_blueprint.route('/gist/<int:gist_id>/comment', methods=['GET'])
def get_gist_comments(gist_id):
    with db.get_db_cursor(True) as cursor:
        cursor.execute(
            "SELECT * FROM gist_comment WHERE gist_id = %s;;", (gist_id,))
        return jsonify(extract_comments_from_cursor(cursor))


@gist_api_blueprint.route('/gist/<int:gist_id>/comment', methods=['POST'])
def create_gist_comments(gist_id):
    content = request.form.get('content')
    user_id = request.form.get('user_id')

    with db.get_db_cursor(True) as cursor:
        try:
            cursor.execute(
                """INSERT INTO gist_comment(content, commented_at, user_id, gist_id)
                VALUES (%s, current_timestamp, %s, %s)
                RETURNING comment_id;""",
                (content, user_id, gist_id))
        
            comment_id = cursor.fetchone()[0]
            current_app.logger.info(
                f"Created new comment: {{'comment_id': {comment_id}, 'gist_id': {gist_id}, 'user_id': {user_id}}}")
            
            # todo: update gist on number of comments

            return {'comment_id': comment_id}
        except Exception as e:
            return jsonify(error=404, text=str(e)), 404


@gist_api_blueprint.route('/gist/<int:gist_id>/fork', methods=['GET'])
def get_gist_forks(gist_id):
    return {}


@gist_api_blueprint.route('/gist/<int:gist_id>/star', methods=['GET'])
def get_gist_stars(gist_id):
    with db.get_db_cursor(True) as cursor:
        cursor.execute("""SELECT gist_user.* FROM star
                          JOIN gist_user ON star.user_id = gist_user.user_id
                          WHERE star.gist_id = %s;""", (gist_id,))
        return jsonify(extract_users_from_cursor(cursor))
