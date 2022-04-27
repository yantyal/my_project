from flask import render_template, redirect, url_for
from flask import request, session
from datetime import datetime
import time
from my_app.models import (create_app, create_error_messages, create_sql_condition,
issue_table, save_file, select_one, select_all, change_tbl, issue_sql, create_hash)


app = create_app()

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            return redirect(url_for('list'))

        end = time.time()
        if 'start' in session:
            # セッションに残すエラー文の生存時間は1秒
            if end - session['start'] >= 1:
                session.clear()
        return render_template('login.html')

    if request.method == 'POST':
        mail_address = request.form['mail_address']
        password = create_hash(request.form['password'])
        sql = issue_sql('login')
        row = select_one(sql, mail_address, password)
        table = issue_table('login')

    # エラー発生時は1で、リダイレクト先を変える
    redirect_number = 0
    if row is not None:
        for t, r in zip(table, row):
            session[t] = r
            if t == 'deleted_datetime' and r is not None:
                redirect_number = 1
    else:
        redirect_number = 1

    if redirect_number == 0:
        return redirect(url_for('list'))
    else:
        session.clear()
        session['errors'] = create_error_messages('login')
        session['start'] = time.time()
        return redirect(url_for('login'))


@app.route('/user/list', methods=['GET','POST'])
def list():
    session.pop('errors', None)

    if 'name' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        sql = issue_sql('list')
        rows = select_all(sql)
    # 社員の検索時にPOSTで受け取る
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        belong_id = request.form['belong_id']
        sql_condition = create_sql_condition(employee_id, name, belong_id)
        sql = issue_sql('sort', sql_condition)
        rows = select_all(sql, employee_id, name, belong_id)

    if rows is None:
        session['errors'] = create_error_messages('sort')
    if len(rows) == 0:
        session['errors'] = create_error_messages('list')

    table = issue_table('list')
    users = []
    for row in rows:
        user = {}
        for t, r in zip(table, row):
            user[t] = r
        users.append(user)
    session["users"] = users

    return render_template('list.html')


@app.route('/user/add', methods=['GET', 'POST'])
def add():
    if 'name' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        end = time.time()
        if 'start' in session:
            # セッションに残すエラー文の生存時間は1秒
            if end - session['start'] >= 1:
                session.pop('errors', None)
                session.pop('start', None)
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
            filename = save_file(file, file.filename, app.config['UPLOAD_FOLDER'])
        sql = issue_sql('login')
        row = select_one(sql, mail_address, password)

    if row is not None:
        session['errors'] = create_error_messages('add')
        session['start'] = time.time()
        return redirect(url_for('add'))

    if not filename and  management != 'Y':
        sql = issue_sql('add', ["0"])
    elif not filename and management == 'Y':
        sql = issue_sql('add', ["1"])
    elif filename and management != 'Y':
        sql = issue_sql('add', ["2"])
    else:
        sql = issue_sql('add', ["3"])
    change_tbl(sql, name, belong_id, mail_address, password, filename, management)

    return redirect(url_for('list'))


@app.route('/user/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    if 'name' not in session:
        return redirect(url_for('login'))

    end = time.time()
    if 'start' in session:
        # セッションに残すエラー文の生存時間は1秒
        if end - session['start'] >= 1:
            session.pop('errors', None)
            session.pop('start', None)

    sql = issue_sql('edit_user_info')
    row = select_one(sql, employee_id)
    table = issue_table('edit')
    user = {}
    if row is not None:
        for t, r in zip(table, row):
            if t == 'image_file_path':
                user[t] = "/static/uploads/" + r
            else:
                user[t] = r
    session['user'] = user
    return render_template('edit.html')


@app.route('/user/result', methods=['POST'])
def edit_result():
    if 'name' not in session:
        return redirect(url_for('login'))

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
        filename = save_file(file, file.filename, app.config['UPLOAD_FOLDER'])
    employee_id = request.form['employee_id']
    sql = issue_sql('edit_check')
    row = select_one(sql, mail_address, password)
    if row is not None:
        row = str(row[0])

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

    change_tbl(sql, name, belong_id, mail_address, password, filename, management, employee_id)

    return redirect(url_for('list'))


@app.route('/user/delete/<employee_id>', methods=['POST'])
def delete(employee_id):
    deleted_datetime = datetime.now().strftime('%Y-%m-%d')
    sql = issue_sql('delete')
    change_tbl(sql, deleted_datetime, employee_id)
    return redirect(url_for('list'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
