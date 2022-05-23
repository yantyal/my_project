from flask import Blueprint, render_template, redirect, url_for
from flask import request, session, current_app
import time
from my_app.models import (check_error_in_session, check_success_in_session, create_error_messages,
create_success_messages, save_file, select_one, change_tbl, issue_sql, issue_table, create_hash,
remove_file, formatter)

edit_bp = Blueprint('edit', __name__, url_prefix='/user', template_folder='my_app.templates')

# 編集
@edit_bp.route('/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    DB_INFO = current_app.config['DB_INFO']

    if 'name' not in session:
        return redirect(url_for('login.login'))

    if str(session['employee_id']) != employee_id and session['management'] != 'Y':
        return redirect(url_for('list.list'))

    check_error_in_session(session, 1)
    check_success_in_session(session, 1)

    sql = issue_sql('edit_user_info')
    row = select_one(DB_INFO, sql, employee_id)
    table = issue_table('edit')
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
        return render_template('edit.html')
    return redirect(url_for('edit.edit', employee_id=employee_id))

# 編集画面からの更新を受け付ける
@edit_bp.route('/result', methods=['POST'])
def edit_result():
    DB_INFO = current_app.config['DB_INFO']
    UPLOAD_FOLDER = current_app.config['UPLOAD_FOLDER']

    if 'name' not in session:
        return redirect(url_for('login.login'))

    if str(session['employee_id']) != str(session['user']['employee_id']) and session['management'] != 'Y':
        return redirect(url_for('list.list'))

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
    # 画像更新の際、以前のファイルを削除する
    if session['user']['image_file_path'] != '' and filename is not None:
        remove_file(session['user']['image_file_path'])
    employee_id = request.form['employee_id']
    sql = issue_sql('edit_check')
    row = select_one(DB_INFO, sql, mail_address, password)
    if row is not None:
        row = str(row[0]) # employee_idを取り出している

    # メールアドレスとパスワードの重複登録は許さないが、
    # 同一ユーザーなら許可(employee_idで検査)
    if row is not None and row != employee_id:
        session['errors'] = create_error_messages('edit')
        session['start'] = time.time()
        formatter.set_employee_id(session)
        current_app.logger.info(session['errors'])
        return redirect(url_for('edit.edit', employee_id=employee_id))

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

    session['success'] = create_success_messages('edit')
    session['success_start'] = time.time()
    formatter.set_employee_id(session)
    current_app.logger.info(session['success'])
    return redirect(url_for('list.list'))

# パスワード変更
@edit_bp.route('/change/password', methods=['POST'])
def change_password():
    DB_INFO = current_app.config['DB_INFO']

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    employee_id = request.form['employee_id']

    if str(session['employee_id']) != employee_id and session['management'] != 'Y':
        return redirect(url_for('list.list'))

    if old_password == "":
        return redirect(url_for('list.list'))
    if new_password == "":
        return redirect(url_for('list.list'))
    if confirm_password == "":
        return redirect(url_for('list.list'))
    if employee_id == "":
        return redirect(url_for('list.list'))

    if new_password != confirm_password:
        session['errors'] = create_error_messages('change_password_new_confirm')
        session['start'] = time.time()
        formatter.set_employee_id(session)
        current_app.logger.info(session['errors'])
        return redirect(url_for('edit.edit', employee_id=employee_id))

    if create_hash(old_password) != session['user']['password']:
        session['errors'] = create_error_messages('change_password_old')
        session['start'] = time.time()
        formatter.set_employee_id(session)
        current_app.logger.info(session['errors'])
        return redirect(url_for('edit.edit', employee_id=employee_id))

    new_password = create_hash(new_password)
    sql = issue_sql('change_password')
    formatter.set_employee_id(session)
    current_app.logger.info(sql)
    change_tbl(DB_INFO, sql, new_password, employee_id)
    session['success'] = create_success_messages('change_password')
    session['success_start'] = time.time()
    formatter.set_employee_id(session)
    current_app.logger.info(session['success'])
    return redirect(url_for('edit.edit', employee_id=employee_id))