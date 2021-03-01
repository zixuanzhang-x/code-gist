from flask import Blueprint, render_template

error_blueprint = Blueprint('error_blueprint', __name__)

@error_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('error_page/404.html'), 404

@error_blueprint.app_errorhandler(410)
def page_gone(e):
    return render_template('error_page/410.html'), 410

@error_blueprint.app_errorhandler(500)
def page_gone(e):
    return render_template('error_page/500.html'), 500
