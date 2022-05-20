from flask import Blueprint, render_template, redirect, url_for
from flask import request, session
import time
from my_app.models import (check_error_in_session, create_error_messages, create_success_messages,
save_file, select_one, change_tbl, issue_sql, create_hash)
from my_app.view import DB_INFO, UPLOAD_FOLDER

add_bp = Blueprint('add', __name__, url_prefix='/user', template_folder='my_app.templates')


# 新規登録
@add_bp.route('/add', methods=['GET', 'POST'])
def add():
    if 'name' not in session:
        return redirect(url_for('login.login'))

    if session['management'] != 'Y':
        return redirect(url_for('list.list'))

    if request.method == 'GET':
        check_error_in_session(session, 1)
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
        sql = issue_sql('add_check')
        row = select_one(DB_INFO, sql, mail_address, password)

    if row is not None:
        session['errors'] = create_error_messages('add')
        session['start'] = time.time()
        return redirect(url_for('add.add'))

    if not filename and  management != 'Y':
        sql = issue_sql('add', ["0"])
    elif not filename and management == 'Y':
        sql = issue_sql('add', ["1"])
    elif filename and management != 'Y':
        sql = issue_sql('add', ["2"])
    else:
        sql = issue_sql('add', ["3"])
    change_tbl(DB_INFO, sql, name, belong_id, mail_address, password, filename, management)

    session['success'] = create_success_messages('add')
    session['success_start'] = time.time()
    return redirect(url_for('list.list'))