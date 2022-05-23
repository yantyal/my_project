from flask import Blueprint, redirect, url_for
from flask import session, current_app
from werkzeug.exceptions import HTTPException
from my_app.models import (Login_user_info, register_messages_in_session, formatter)

exception_bp = Blueprint('exception', __name__, template_folder='my_app.templates')

# 404エラーハンドラー # 405エラーハンドラー
@exception_bp.errorhandler(404)
@exception_bp.errorhandler(405)
def page_not_found(error):
    register_messages_in_session(session, 'errors', '404')
    formatter.set_employee_id(session)
    current_app.logger.info(session['errors'])
    if Login_user_info.name.value not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('list.list'))


# 汎用的なエラーハンドラー
@exception_bp.errorhandler(HTTPException)
def error_handler(error):
    register_messages_in_session(session, 'errors', 'error')
    formatter.set_employee_id(session)
    current_app.logger.info(session['errors'])
    if Login_user_info.name.value not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('list.list'))
