from flask import Flask, render_template, redirect, url_for
from flask import request, session
from datetime import timedelta, datetime
import time
from my_app.models import create_error_messages, create_sql_condition, issue_table, select_one, select_all, change_tbl, issue_sql

app = Flask(__name__)
app.secret_key = 'abcdefghijklmn'
app.permanent_session_lifetime = timedelta(minutes=3) # セッションの生存時間は3分

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            return redirect(url_for('list'))
        else:
            end = time.time()
            if 'start' in session:
                # セッションに残すエラー文の生存時間は1秒
                if end - session['start'] >= 1:
                    session.clear()
            return render_template('login.html')

    if request.method == 'POST':
        mail_address = request.form['mail_address']
        password = request.form['password']
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
    # POSTで受け取るのは社員の検索時
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
    if 'name' in session:
        if request.method == 'POST':
            name = request.form['name']
            belong_id = request.form['belong_id']
            mail_address = request.form['mail_address']
            password = request.form['password']
            management = request.form.getlist('management')
            if len(management) != 0:
                management = management[0]
            sql = issue_sql('login')
            row = select_one(sql, mail_address, password)
            if row is None:
                if management == 'Y':
                    sql = issue_sql('add', ["0"])
                    change_tbl(sql, name, belong_id, mail_address, password, management)
                else:
                    sql = issue_sql('add', ["1"])
                    change_tbl(sql, name, belong_id, mail_address, password)
            else:
                error_messages = create_error_messages('add')
                return render_template('add.html', error_messages=error_messages)
            return redirect(url_for('list'))
        else:
            error_messages = []
            return render_template('add.html', error_messages=error_messages)
    else:
        return redirect(url_for('login'))

@app.route('/user/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    if 'name' in session:
        sql = issue_sql('edit_user_info')
        row = select_one(sql, employee_id)
        table = issue_table('edit')
        error_messages = []
        user = {}
        if row is not None:
            for t, r in zip(table, row):
                user[t] = r
        return render_template('edit.html', error_messages=error_messages, user=user)
    else:
        return redirect(url_for('login'))

@app.route('/user/result', methods=['POST'])
def edit_result():
    if 'name' in session:
        name = request.form['name']
        belong_id = request.form['belong_id']
        mail_address = request.form['mail_address']
        password = request.form['password']
        management = request.form.getlist('management')
        employee_id = request.form['employee_id']
        sql = issue_sql('edit_check')
        row = select_one(sql, mail_address, password)
        if row is None or row == employee_id:
            if len(management) != 0:
                management = management[0]
                sql = issue_sql('edit', ["0"])
            else:
                management = None
                sql = issue_sql('edit', ["1"])
        else:
            return redirect(url_for('list'))
        change_tbl(sql, name, belong_id, mail_address, password, management, employee_id)
        return redirect(url_for('list'))
    else:
        return redirect(url_for('login'))

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
