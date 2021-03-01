from utils.time_util import convertTimezone
from datetime import datetime


def extract_users_from_cursor(cursor):
    return [{
            'user_id': result[0],
            'auth0_id': result[1],
            'user_name': result[2],
            'picture': result[3],
            } for result in cursor]


def extract_gists_from_cursor(cursor):
    return [{
            'gist_id': record[0],
            'user_id': record[1],
            'gist_name': record[2],
            'user_name': record[3],
            'description': record[4],
            'content': record[5],
            'created': convertTimezone(str(record[6])),
            'last_modified': convertTimezone(str(record[7])),
            'stars': record[8],
            'comments': record[9],
            } for record in cursor]


def extract_comments_from_cursor(cursor):
    comments = [{
        'comment_id': record[0],
        'content': record[1],
        'commented_at': convertTimezone(str(record[2])),
        'user_id': record[3],
        'gist_id': record[4],
    } for record in cursor]
    comments.sort(key=lambda comment: datetime.strptime(
        comment['commented_at'], '%Y-%m-%d %H:%M:%S'))
    return comments
