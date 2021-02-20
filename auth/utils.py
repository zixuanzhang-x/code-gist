from flask import redirect, session, url_for
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated
