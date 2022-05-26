from flask import Blueprint, redirect, url_for
from flask import session, current_app
from datetime import datetime
from my_app.enum import transition_redirect_target
from my_app.models import (Login_user_info, change_tbl, issue_sql, register_messages_in_session,
formatter)

delete_bp = Blueprint('delete', __name__, url_prefix='/user', template_folder='my_app.templates')


# 削除前処理
@delete_bp.before_request
def user_load():
    if session[Login_user_info.management.value] != 'Y':
        return redirect(url_for(transition_redirect_target.LIST.value))


# 削除(実際にはデータは削除しない)
@delete_bp.route('/delete/<employee_id>', methods=['POST'])
def delete(employee_id):
    DB_INFO = current_app.config['DB_INFO']

    deleted_datetime = datetime.now().strftime('%Y-%m-%d')
    sql = issue_sql('delete')
    change_tbl(DB_INFO, sql, deleted_datetime, employee_id)
    formatter.set_employee_id(session)
    current_app.logger.info(sql)
    register_messages_in_session(session, 'success', 'delete')
    return redirect(url_for(transition_redirect_target.LIST.value))