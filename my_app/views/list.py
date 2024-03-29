from flask import Blueprint, render_template, redirect, url_for
from flask import request, session, current_app
from my_app.enum import (transition_redirect_target, transition_render_template_target,
Login_user_info, sql_name, table_name)
from my_app.models import (check_error_in_session, check_sort_placeholder_in_session, check_success_in_session,
create_sql_condition, create_users, issue_table, register_messages_in_session, register_sort_placeholder_in_session, select_all,
issue_sql, formatter)

list_bp = Blueprint('list', __name__, url_prefix='/user', template_folder='my_app.templates')

# 社員一覧リスト前処理
@list_bp.before_request
def user_load():
    if Login_user_info.NAME.value not in session:
        return redirect(url_for(transition_redirect_target.LOGIN.value))

# 社員一覧リスト
@list_bp.route('/list', methods=['GET','POST'])
def list():
    DB_INFO = current_app.config['DB_INFO']

    if request.method == 'GET':
        check_error_in_session(session, 0.2)
        check_success_in_session(session)
        check_sort_placeholder_in_session(session)
        if 'sort' in session:
            if session['sort'] == 'sort':
                session.pop('sort', None)
                return render_template(transition_render_template_target.LIST.value)
        sql = issue_sql(sql_name.LIST.value)
        rows = select_all(DB_INFO, sql)
        table = issue_table(table_name.LIST.value)
        session["users"] = create_users(table, rows)
        formatter.set_employee_id(session)
        current_app.logger.info(sql)
        return render_template(transition_render_template_target.LIST.value)
    # 社員の検索時にPOSTで受け取る
    if request.method == 'POST':
        sort_employee_id = ''
        sort_name = ''
        belong_id = ''
        if 'sort' in request.form:
            sort = request.form['sort']
            if sort == '':
                return redirect(url_for(transition_redirect_target.LIST.value))
            sort_employee_id = sort
            sort_name = '%' + sort + '%'
        register_sort_placeholder_in_session(session, sort_employee_id)
        if 'belong_id' in request.form:
            belong_id = request.form['belong_id']
        sql_condition = create_sql_condition(sort_employee_id, sort_name, belong_id)
        sql = issue_sql(sql_name.SORT.value, sql_condition)
        rows = select_all(DB_INFO, sql, sort_employee_id, sort_name, belong_id)
        formatter.set_employee_id(session)
        current_app.logger.info(sql)

    if rows is None:
        register_messages_in_session(session, 'errors', 'sort')
        formatter.set_employee_id(session)
        current_app.logger.info('Logout.')
        return redirect(url_for(transition_redirect_target.LIST.value))
    if len(rows) == 0:
        register_messages_in_session(session, 'errors', 'list')
        formatter.set_employee_id(session)
        current_app.logger.info('Logout.')

    table = issue_table(table_name.LIST.value)
    session["users"] = create_users(table, rows)

    session['sort'] = 'sort'
    return redirect(url_for(transition_redirect_target.LIST.value))