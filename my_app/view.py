from flask import render_template, redirect, url_for, make_response
from flask import request, session
from werkzeug.exceptions import HTTPException
from datetime import datetime
import time, json, logging
from my_app.models import (check_error_in_session, check_success_in_session, create_app, create_error_messages, create_sql_condition, create_success_messages, create_users,
issue_table, save_file, select_one, select_all, change_tbl, issue_sql, create_hash, formatter)


app = create_app()

DB_INFO = app.config['DB_INFO']
LOGFILE = app.config['LOGFILE']
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

log_handler = logging.FileHandler(LOGFILE)
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)

from my_app.views.login import login_bp
app.register_blueprint(login_bp)
from my_app.views.list import list_bp
app.register_blueprint(list_bp)
from my_app.views.add import add_bp
app.register_blueprint(add_bp)


@app.route('/')
def index():
    app.logger.info('From Index To Login.')
    return redirect(url_for('login.login'))


# 編集
@app.route('/user/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    if 'name' not in session:
        return redirect(url_for('login.login'))

    if str(session['employee_id']) != employee_id and session['management'] != 'Y':
        return redirect(url_for('list'))

    check_error_in_session(session, 1)
    check_success_in_session(session, 1)

    sql = issue_sql('edit_user_info')
    row = select_one(DB_INFO, sql, employee_id)
    table = issue_table('edit')
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
    return redirect(url_for('edit', employee_id=employee_id))

# 編集画面からの更新を受け付ける
@app.route('/user/result', methods=['POST'])
def edit_result():
    if 'name' not in session:
        return redirect(url_for('login.login'))

    if str(session['employee_id']) != str(session['user']['employee_id']) and session['management'] != 'Y':
        return redirect(url_for('list'))

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
        return redirect(url_for('edit', employee_id=employee_id))

    if not filename and  management != 'Y':
        sql = issue_sql('edit', ["0"])
    elif not filename and management == 'Y':
        sql = issue_sql('edit', ["1"])
    elif filename and management != 'Y':
        sql = issue_sql('edit', ["2"])
    else:
        sql = issue_sql('edit', ["3"])

    change_tbl(DB_INFO, sql, name, belong_id, mail_address, password, filename, management, employee_id)

    session['success'] = create_success_messages('edit')
    session['success_start'] = time.time()
    return redirect(url_for('list'))

# パスワード変更
@app.route('/change/password', methods=['POST'])
def change_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    employee_id = request.form['employee_id']

    if str(session['employee_id']) != employee_id and session['management'] != 'Y':
        return redirect(url_for('list'))

    if old_password == "":
        return redirect(url_for('list'))
    if new_password == "":
        return redirect(url_for('list'))
    if confirm_password == "":
        return redirect(url_for('list'))
    if employee_id == "":
        return redirect(url_for('list'))

    if new_password != confirm_password:
        session['errors'] = create_error_messages('change_password_new_confirm')
        session['start'] = time.time()
        return redirect(url_for('edit', employee_id=employee_id))

    if create_hash(old_password) != session['user']['password']:
        session['errors'] = create_error_messages('change_password_old')
        session['start'] = time.time()
        return redirect(url_for('edit', employee_id=employee_id))

    new_password = create_hash(new_password)
    sql = issue_sql('change_password')
    change_tbl(DB_INFO, sql, new_password, employee_id)
    session['success'] = create_success_messages('change_password')
    session['success_start'] = time.time()
    return redirect(url_for('edit', employee_id=employee_id))

# 削除(実際にはデータは削除しない)
@app.route('/user/delete/<employee_id>', methods=['POST'])
def delete(employee_id):
    if session['management'] != 'Y':
        return redirect(url_for('list'))

    deleted_datetime = datetime.now().strftime('%Y-%m-%d')
    sql = issue_sql('delete')
    change_tbl(DB_INFO, sql, deleted_datetime, employee_id)
    return redirect(url_for('list'))

# ログアウト
@app.route('/logout')
def logout():
    formatter.set_employee_id(session)
    app.logger.info('Logout.')
    session.clear()
    return redirect(url_for('login.login'))

# 404エラーハンドラー # 405エラーハンドラー
@app.errorhandler(404)
@app.errorhandler(405)
def page_not_found(error):
    session['errors'] = create_error_messages('404')
    session['start'] = time.time()
    if 'name' not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('list'))

# 汎用的なエラーハンドラー
@app.errorhandler(HTTPException)
def error_handler(error):
    session['errors'] = create_error_messages('error')
    session['start'] = time.time()
    if 'name' not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('list'))