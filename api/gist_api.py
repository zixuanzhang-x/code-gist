from flask import Blueprint, request, current_app, jsonify
from db import db
from utils.api_util import extract_gists_from_cursor, extract_comments_from_cursor, extract_users_from_cursor

gist_api_blueprint = Blueprint('gist_api_blueprint', __name__)


@gist_api_blueprint.route('/gist', methods=['GET'])
def get_gists():
    """
    Returns a list of gists whose gist_name matchs 'q'.
    All gists are matched if q is not provided.
    """
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
    """Create a new gist."""
    user_id = request.form.get('user_id')
    gist_name = request.form.get('gist_name')
    user_name = request.form.get('user_name')
    description = request.form.get('description')
    content = request.form.get('content')
    with db.get_db_cursor(True) as cursor:
        cursor.execute(
            """INSERT INTO gist(user_id,
                                gist_name,
                                user_name, 
                                description,
                                content, 
                                created,
                                last_modified)
               VALUES (%s, %s, %s, %s, %s, current_timestamp, current_timestamp)
               RETURNING user_id;""",
            (user_id, gist_name, user_name, description, content))
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
    with db.get_db_cursor(True) as cursor:
        cursor.execute("SELECT * FROM gist WHERE gist_id = %s;;", (gist_id,))
        if cursor.rowcount == 0:
            return jsonify(error=400, text='gist_id not found'), 400
        else:
            gist = extract_gists_from_cursor(cursor)[0]
            gist_name = request.form.get('gist_name')
            description = request.form.get('description')
            content = request.form.get('content')

            cursor.execute("""UPDATE gist
                              SET gist_name = %s,
                                  description = %s,
                                  content = %s,
                                  last_modified = current_timestamp
                              WHERE gist_id = %s;""", (gist_name or gist['gist_name'],
                                                       description or gist['description'],
                                                       content or gist['content'],
                                                       gist_id))

            cursor.execute("SELECT * FROM gist WHERE gist_id = %s;;", (gist_id,))
            return jsonify(extract_gists_from_cursor(cursor))


@gist_api_blueprint.route('/gist/<int:gist_id>/comment', methods=['GET'])
def get_gist_comments(gist_id):
    """Return a list of comments of this gist."""
    with db.get_db_cursor(True) as cursor:
        cursor.execute(
            "SELECT * FROM gist_comment WHERE gist_id = %s;;", (gist_id,))
        return jsonify(extract_comments_from_cursor(cursor))


@gist_api_blueprint.route('/gist/<int:gist_id>/comment', methods=['POST'])
def create_gist_comments(gist_id):
    """Create a new comment under this gist."""
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

            cursor.execute("UPDATE gist SET comments = comments + 1 WHERE gist_id = %s", (gist_id,))

            return {'comment_id': comment_id}
        except Exception as e:
            return jsonify(error=400, text=str(e)), 400


@gist_api_blueprint.route('/gist/<int:gist_id>/star', methods=['GET'])
def get_gist_stars(gist_id):
    """Return a list of users that starred this gist"""
    with db.get_db_cursor(True) as cursor:
        cursor.execute("""SELECT gist_user.* FROM star
                          JOIN gist_user ON star.user_id = gist_user.user_id
                          WHERE star.gist_id = %s;""", (gist_id,))
        return jsonify(extract_users_from_cursor(cursor))


@gist_api_blueprint.route('/gist/<int:gist_id>/star', methods=['POST'])
def create_gist_star(gist_id):
    """Create a star relationship between a user and this gist"""
    user_id = request.form.get('user_id')
    with db.get_db_cursor(True) as cursor:
        try:
            cursor.execute(
                "INSERT INTO star(user_id, gist_id) VALUES (%s, %s);", (user_id, gist_id))

            current_app.logger.info(
                f"""Created new star: {{'user_id': {user_id}, 'gist_id': {gist_id}}}""")

            cursor.execute("UPDATE gist SET stars = stars + 1 WHERE gist_id = %s", (gist_id,))

            return {'user_id': user_id, 'gist_id': gist_id}
        except Exception as e:
            return jsonify(error=400, text=str(e)), 400
        

@gist_api_blueprint.route('/gist/<int:gist_id>/star', methods=['DELETE'])
def delete_gist_star(gist_id):
    """Delete a star relationship between a user and this gist"""
    user_id = request.form.get('user_id')
    with db.get_db_cursor(True) as cursor:
        try:
            cursor.execute(
                "DELETE FROM star WHERE user_id = %s AND gist_id = %s;", (user_id, gist_id))

            current_app.logger.info(
                f"""Deleted an old star: {{'user_id': {user_id}, 'gist_id': {gist_id}}}""")

            cursor.execute("UPDATE gist SET stars = stars - 1 WHERE gist_id = %s", (gist_id,))

            return {'user_id': user_id, 'gist_id': gist_id}
        except Exception as e:
            return jsonify(error=400, text=str(e)), 400