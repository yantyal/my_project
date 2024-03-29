from flask import Blueprint, redirect, url_for
from flask import session, current_app
from werkzeug.exceptions import HTTPException
from my_app.enum import (transition_redirect_target, Login_user_info)
from my_app.models import (register_messages_in_session, formatter)

exception_bp = Blueprint('exception', __name__, template_folder='my_app.templates')

# 404エラーハンドラー # 405エラーハンドラー
@exception_bp.errorhandler(404)
@exception_bp.errorhandler(405)
def page_not_found(error):
    register_messages_in_session(session, 'errors', '404')
    formatter.set_employee_id(session)
    current_app.logger.info(session['errors'])
    if Login_user_info.NAME.value not in session:
        return redirect(url_for(transition_redirect_target.LOGIN.value))
    return redirect(url_for(transition_redirect_target.LIST.value))


# 汎用的なエラーハンドラー
@exception_bp.errorhandler(HTTPException)
def error_handler(error):
    register_messages_in_session(session, 'errors', 'error')
    formatter.set_employee_id(session)
    current_app.logger.info(session['errors'])
    if Login_user_info.NAME.value not in session:
        return redirect(url_for(transition_redirect_target.LOGIN.value))
    return redirect(url_for(transition_redirect_target.LIST.value))
