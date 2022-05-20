from flask import Blueprint, render_template, redirect, url_for
from flask import request, session
import time
from my_app.models import (check_error_in_session, check_success_in_session, create_error_messages,
create_sql_condition, create_users, issue_table, select_all, issue_sql)
from my_app.view import DB_INFO

list_bp = Blueprint('list', __name__, url_prefix='/user', template_folder='my_app.templates')

# 社員一覧リスト
@list_bp.route('/list', methods=['GET','POST'])
def list():
    if 'name' not in session:
        return redirect(url_for('login.login'))

    if request.method == 'GET':
        check_error_in_session(session, 0.2)
        check_success_in_session(session, 1)
        if 'sort' in session:
            if session['sort'] == 'sort':
                session.pop('sort', None)
                return render_template('list.html')
        sql = issue_sql('list')
        rows = select_all(DB_INFO, sql)
        table = issue_table('list')
        session["users"] = create_users(table, rows)
        return render_template('list.html')
    # 社員の検索時にPOSTで受け取る
    if request.method == 'POST':
        sort_employee_id = ''
        sort_name = ''
        belong_id = ''
        if 'sort' in request.form:
            sort = request.form['sort']
            if sort == '':
                return redirect(url_for('list.list'))
            sort_employee_id = sort
            sort_name = '%' + sort + '%'
        if 'belong_id' in request.form:
            belong_id = request.form['belong_id']
        sql_condition = create_sql_condition(sort_employee_id, sort_name, belong_id)
        sql = issue_sql('sort', sql_condition)
        rows = select_all(DB_INFO, sql, sort_employee_id, sort_name, belong_id)

    if rows is None:
        session['errors'] = create_error_messages('sort')
        session['start'] = time.time()
    if len(rows) == 0:
        session['errors'] = create_error_messages('list')
        session['start'] = time.time()

    table = issue_table('list')
    session["users"] = create_users(table, rows)

    session['sort'] = 'sort'
    return redirect(url_for('list.list'))