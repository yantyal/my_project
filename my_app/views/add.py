from flask import Blueprint, render_template, redirect, url_for
from flask import request, session, current_app
from my_app.models import (Add_sql_condition, Login_user_info, check_error_in_session, check_success_in_session, register_messages_in_session,
save_file, select_one, change_tbl, issue_sql, create_hash, formatter)

add_bp = Blueprint('add', __name__, url_prefix='/user', template_folder='my_app.templates')


# 新規登録前処理
@add_bp.before_request
def user_load():
    if Login_user_info.name.value not in session:
        return redirect(url_for('login.login'))

    if session[Login_user_info.management.value] != 'Y':
        return redirect(url_for('list.list'))


# 新規登録
@add_bp.route('/add', methods=['GET', 'POST'])
def add():
    DB_INFO = current_app.config['DB_INFO']
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    if request.method == 'GET':
        check_error_in_session(session)
        check_success_in_session(session)
        return render_template('add.html')
    # 新規登録時にPOSTで受け取る
    if request.method == 'POST':
        name = request.form['name']
        belong_id = request.form['belong_id']
        mail_address = request.form['mail_address']
        password = create_hash(request.form['password'])
        management = request.form.getlist('management')
        if len(management) != 0:
            management = management[0]
        else:
            management = None
        filename = None
        if 'file' in request.files:
            file = request.files['file']
        if file.filename != '':
            filename = save_file(file, file.filename, UPLOAD_FOLDER)
        if file.filename == filename:
            register_messages_in_session(session, 'errors', 'file')
            filename = None
        sql = issue_sql('add_check')
        row = select_one(DB_INFO, sql, mail_address, password)
        formatter.set_employee_id(session)
        current_app.logger.info(sql)

    if row is not None:
        register_messages_in_session(session, 'errors', 'add')
        formatter.set_employee_id(session)
        current_app.logger.info(session['errors'])
        return redirect(url_for('add.add'))

    if not filename and  management != 'Y':
        sql = issue_sql('add', Add_sql_condition.not_exist_filename_and_management.value)
    elif not filename and management == 'Y':
        sql = issue_sql('add', Add_sql_condition.exist_management.value)
    elif filename and management != 'Y':
        sql = issue_sql('add', Add_sql_condition.exist_filename.value)
    else:
        sql = issue_sql('add', Add_sql_condition.exist_filename_and_management.value)
    change_tbl(DB_INFO, sql, name, belong_id, mail_address, password, filename, management)

    register_messages_in_session(session, 'success', 'add')
    formatter.set_employee_id(session)
    current_app.logger.info(session['success'])
    return redirect(url_for('list.list'))