from flask import Blueprint

error_blueprint = Blueprint('error_blueprint', __name__)

@error_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@error_blueprint.errorhandler(410)
def page_gone(e):
    return render_template('410.html'), 410
