from flask import Blueprint, redirect, url_for
from flask import session, current_app
from werkzeug.exceptions import HTTPException
import time
from my_app.models import (create_error_messages, formatter)

exception_bp = Blueprint('exception', __name__, template_folder='my_app.templates')

# 404エラーハンドラー # 405エラーハンドラー
@exception_bp.errorhandler(404)
@exception_bp.errorhandler(405)
def page_not_found(error):
    session['errors'] = create_error_messages('404')
    session['start'] = time.time()
    formatter.set_employee_id(session)
    current_app.logger.info(session['errors'])
    if 'name' not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('list.list'))


# 汎用的なエラーハンドラー
@exception_bp.errorhandler(HTTPException)
def error_handler(error):
    session['errors'] = create_error_messages('error')
    session['start'] = time.time()
    formatter.set_employee_id(session)
    current_app.logger.info(session['errors'])
    if 'name' not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('list.list'))
