from flask import Blueprint, render_template, redirect, url_for
from flask import request, session, current_app
from my_app.enum import (transition_redirect_target, transition_render_template_target,
Login_user_info, sql_name, table_name)
from my_app.models import (check_employee_id, check_error_in_session, check_success_in_session, register_messages_in_session,
save_file, select_one, change_tbl, issue_sql, issue_table, create_hash, remove_file, formatter)

edit_bp = Blueprint('edit', __name__, url_prefix='/user', template_folder='my_app.templates')


# 編集前処理
@edit_bp.before_request
def user_load():
    if Login_user_info.NAME.value not in session:
        return redirect(url_for(transition_redirect_target.LOGIN.value))


# 編集
@edit_bp.route('/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    DB_INFO = current_app.config['DB_INFO']

    if str(session[Login_user_info.EMPLOYEE_ID.value]) != employee_id and session[Login_user_info.MANAGEMENT.value] != 'Y':
        return redirect(url_for(transition_redirect_target.LIST.value))
    check_employee_id(employee_id)

    check_error_in_session(session)
    check_success_in_session(session)

    sql = issue_sql(sql_name.EDIT_USER_INFO.value)
    row = select_one(DB_INFO, sql, employee_id)
    table = issue_table(table_name.EDIT.value)
    formatter.set_employee_id(session)
    current_app.logger.info(sql)
    user = {}
    if row is not None:
        for t, r in zip(table, row):
            if t == 'image_file_path':
                user[t] = "/static/uploads/" + r
            else:
                user[t] = r
    session['user'] = user

    if request.method == 'GET':
        return render_template(transition_render_template_target.EDIT.value)
    return redirect(url_for(transition_redirect_target.EDIT.value, employee_id=employee_id))

# 編集画面からの更新を受け付ける
@edit_bp.route('/result', methods=['POST'])
def edit_result():
    DB_INFO = current_app.config['DB_INFO']
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    if str(session[Login_user_info.EMPLOYEE_ID.value]) != str(session['user']['employee_id']) and session[Login_user_info.MANAGEMENT.value] != 'Y':
        return redirect(url_for(transition_redirect_target.LIST.value))

    name = request.form['name']
    belong_id = request.form['belong_id']
    mail_address = request.form['mail_address']
    plane = request.form['password']
    if plane == '':
        password = session['user']['password']
    else:
        password = create_hash(plane)
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
    # 画像更新の際、以前のファイルを削除する
    if session['user']['image_file_path'] != '/static/uploads/' and filename is not None:
        remove_file(session['user']['image_file_path'])
    employee_id = request.form['employee_id']
    sql = issue_sql(sql_name.EDIT_CHECK.value)
    row = select_one(DB_INFO, sql, mail_address, password)
    if row is not None:
        row = str(row[0]) # employee_idを取り出している

    # メールアドレスとパスワードの重複登録は許さないが、
    # 同一ユーザーなら許可(employee_idで検査)
    if row is not None and row != employee_id:
        register_messages_in_session(session, 'errors', 'edit')
        formatter.set_employee_id(session)
        current_app.logger.info(session['errors'])
        return redirect(url_for(transition_redirect_target.EDIT.value, employee_id=employee_id))

    if not filename and  management != 'Y':
        sql = issue_sql('edit', ["0"])
    elif not filename and management == 'Y':
        sql = issue_sql('edit', ["1"])
    elif filename and management != 'Y':
        sql = issue_sql('edit', ["2"])
    else:
        sql = issue_sql('edit', ["3"])

    formatter.set_employee_id(session)
    current_app.logger.info(sql)
    change_tbl(DB_INFO, sql, name, belong_id, mail_address, password, filename, management, employee_id)

    register_messages_in_session(session, 'success', 'edit')
    formatter.set_employee_id(session)
    current_app.logger.info(session['success'])
    return redirect(url_for(transition_redirect_target.LIST.value))

# パスワード変更
@edit_bp.route('/change/password', methods=['POST'])
def change_password():
    DB_INFO = current_app.config['DB_INFO']

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    employee_id = request.form['employee_id']

    if str(session[Login_user_info.EMPLOYEE_ID.value]) != employee_id and session[Login_user_info.MANAGEMENT.value] != 'Y':
        return redirect(url_for(transition_redirect_target.LIST.value))

    if old_password == "" or new_password == "" or confirm_password == "" or employee_id == "":
        return redirect(url_for(transition_redirect_target.LIST.value))

    if new_password != confirm_password:
        register_messages_in_session(session, 'errors', 'change_password_new_confirm')
        formatter.set_employee_id(session)
        current_app.logger.info(session['errors'])
        return redirect(url_for(transition_redirect_target.EDIT.value, employee_id=employee_id))

    if create_hash(old_password) != session['user']['password']:
        register_messages_in_session(session, 'errors', 'change_password_old')
        formatter.set_employee_id(session)
        current_app.logger.info(session['errors'])
        return redirect(url_for(transition_redirect_target.EDIT.value, employee_id=employee_id))

    new_password = create_hash(new_password)
    sql = issue_sql(sql_name.CHANGE_PASSWORD.value)
    formatter.set_employee_id(session)
    current_app.logger.info(sql)
    change_tbl(DB_INFO, sql, new_password, employee_id)
    register_messages_in_session(session, 'success', 'change_password')
    formatter.set_employee_id(session)
    current_app.logger.info(session['success'])
    return redirect(url_for(transition_redirect_target.EDIT.value, employee_id=employee_id))