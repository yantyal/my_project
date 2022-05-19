from flask import render_template, redirect, url_for, make_response
from flask import request, session
from werkzeug.exceptions import HTTPException
from datetime import datetime
import time, json
from my_app.models import (check_error_in_session, check_success_in_session, create_app, create_error_messages, create_sql_condition, create_success_messages, create_users,
issue_table, save_file, select_one, select_all, change_tbl, issue_sql, create_hash)


app = create_app()

@app.route('/')
def index():
    return redirect(url_for('login'))

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            return redirect(url_for('list'))

        user_info = request.cookies.get('user_info')
        if user_info is None:
            check_error_in_session(session, 1)
            return render_template('login.html')

        # クッキーにユーザー情報があればログイン
        user_info = json.loads(user_info)
        mail_address = user_info['mail_address']
        password = user_info['password']
        sql = issue_sql('login')
        row = select_one(sql, mail_address, password)
        table = issue_table('login')

        # ログインが拒否された場合はリダイレクト先を変える
        # 社員一覧リスト(0) ログイン画面(1)
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
            return render_template('login.html')

    if request.method == 'POST':
        mail_address = request.form['mail_address']
        password = create_hash(request.form['password'])
        check_cookie = request.form.getlist('check_cookie')
        if len(check_cookie) != 0:
            check_cookie = check_cookie[0]
        sql = issue_sql('login')
        row = select_one(sql, mail_address, password)
        table = issue_table('login')

    # ログインが拒否された場合はリダイレクト先を変える
    # 社員一覧リスト(0) ログイン画面(1)
    redirect_number = 0
    if row is not None:
        for t, r in zip(table, row):
            session[t] = r
            if t == 'deleted_datetime' and r is not None:
                redirect_number = 1
    else:
        redirect_number = 1

    if redirect_number == 1:
        session.clear()
        session['errors'] = create_error_messages('login')
        session['start'] = time.time()
        return redirect(url_for('login'))

    if check_cookie == 'ok':
        max_age = 30 # クッキーの生存時間は30秒
        expires = int(datetime.now().timestamp()) + max_age
        response = make_response(redirect(url_for('list')))
        user_info = {'mail_address': mail_address, 'password': password}
        response.set_cookie("user_info", value=json.dumps(user_info), expires=expires)
        return response
    else:
        return redirect(url_for('list'))

# 社員一覧リスト
@app.route('/user/list', methods=['GET','POST'])
def list():
    if 'name' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        check_error_in_session(session, 0.2)
        if 'sort' in session:
            if session['sort'] == 'sort':
                session.pop('sort', None)
                return render_template('list.html')
        sql = issue_sql('list')
        rows = select_all(sql)
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
                return redirect(url_for('list'))
            sort_employee_id = sort
            sort_name = '%' + sort + '%'
        if 'belong_id' in request.form:
            belong_id = request.form['belong_id']
        sql_condition = create_sql_condition(sort_employee_id, sort_name, belong_id)
        sql = issue_sql('sort', sql_condition)
        rows = select_all(sql, sort_employee_id, sort_name, belong_id)

    if rows is None:
        session['errors'] = create_error_messages('sort')
        session['start'] = time.time()
    if len(rows) == 0:
        session['errors'] = create_error_messages('list')
        session['start'] = time.time()

    table = issue_table('list')
    session["users"] = create_users(table, rows)

    session['sort'] = 'sort'
    return redirect(url_for('list'))

# 新規登録
@app.route('/user/add', methods=['GET', 'POST'])
def add():
    if 'name' not in session:
        return redirect(url_for('login'))

    if session['management'] != 'Y':
        return redirect(url_for('list'))

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
            filename = save_file(file, file.filename, app.config['UPLOAD_FOLDER'])
        sql = issue_sql('add_check')
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

# 編集
@app.route('/user/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    if 'name' not in session:
        return redirect(url_for('login'))

    if str(session['employee_id']) != employee_id and session['management'] != 'Y':
        return redirect(url_for('list'))

    check_error_in_session(session, 1)
    check_success_in_session(session, 1)

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

    if request.method == 'GET':
        return render_template('edit.html')
    return redirect(url_for('edit', employee_id=employee_id))

# 編集画面からの更新を受け付ける
@app.route('/user/result', methods=['POST'])
def edit_result():
    if 'name' not in session:
        return redirect(url_for('login'))

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
        filename = save_file(file, file.filename, app.config['UPLOAD_FOLDER'])
    employee_id = request.form['employee_id']
    sql = issue_sql('edit_check')
    row = select_one(sql, mail_address, password)
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

    change_tbl(sql, name, belong_id, mail_address, password, filename, management, employee_id)

    session['success'] = create_success_messages('edit')
    session['success_start'] = time.time()
    # return redirect(url_for('list'))
    # TODO 社員一覧リストに成功文を出すか検証
    return redirect(url_for('edit', employee_id=employee_id))

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
    change_tbl(sql, new_password, employee_id)
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
    change_tbl(sql, deleted_datetime, employee_id)
    return redirect(url_for('list'))

# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
