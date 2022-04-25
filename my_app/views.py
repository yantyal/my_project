from flask import Flask, render_template, redirect, url_for
from flask import request, session
from datetime import timedelta, datetime
import time
from my_app.models import create_dict_list, select_one, select_all, change_tbl, issue_sql

app = Flask(__name__)
app.secret_key = 'abcdefghijklmn'
app.permanent_session_lifetime = timedelta(minutes=3) # sessionの生存時間

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail_address = request.form['mail_address']
        password = request.form['password']
        sql = issue_sql('login')
        row = select_one(sql, mail_address, password)
        tbl = ['employee_id', 'name', 'deleted_datetime', 'management']
        errors = ['ログインに失敗しました。',
                'メールアドレスとパスワードをご確認ください。']
        if row is not None:
            for t, r in zip(tbl, row):
                session[t] = r
                if t == 'deleted_datetime' and r is not None:
                    session.clear()
                    session['errors'] = errors
                    session['start'] = time.time()
                    return redirect(url_for('login'))
            return redirect(url_for('list'))
        else:
            #TODOトークンを利用する
            session['errors'] = errors
            session['start'] = time.time()
            return redirect(url_for('login'))
    else:
        if 'name' in session:
            return redirect(url_for('list'))
        else:
            end = time.time()
            if 'start' in session:
                # セッションに残すエラー文の生存時間は3秒
                if end - session['start'] >= 3:
                    session.clear()
            return render_template('login.html')

@app.route('/user/list', methods=['GET','POST'])
def list():
    if 'name' in session:
        sql = ''
        if request.method == 'GET':
            sql = issue_sql('list')
            rows = select_all(sql)
        else:
            employee_id = request.form['employee_id']
            name = request.form['name']
            belong_id = request.form['belong_id']
            dict_list = create_dict_list(employee_id, name, belong_id)
            sql = issue_sql('sort', dict_list)
            rows = select_all(sql, employee_id, name, belong_id)
        tbl = ['employee_id', 'name', 'mail_address', 'password', 'management',
                'deleted_datetime', 'image_file_path','belong_id', 'belong_name']
        users = []
        errors = []
        if rows is not None:
            if len(rows) == 0:
                errors = ['リストに存在しません']
                return render_template('list.html', errors=errors, users=users)
            for row in rows:
                user = {}
                for t, r in zip(tbl, row):
                    user[t] = r
                users.append(user)
        else:
            errors = ['リストの取得に失敗しました。']
            return render_template('list.html', errors=errors, users=users)
        return render_template('list.html', errors=errors, users=users)
    else:
        return redirect(url_for('login'))

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
                errors = ['登録できないメールアドレスと',
                        'パスワードです']
                return render_template('add.html', errors=errors)
            return redirect(url_for('list'))
        else:
            errors = []
            return render_template('add.html',errors=errors)
    else:
        return redirect(url_for('login'))

@app.route('/user/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    if 'name' in session:
        sql = "select e.employee_id, e.name, e.belong_id, e.mail_address, e.password, \
            e.management, b.belong_name\
            from employee_tbl as e inner join belong_master_tbl as b \
            where e.belong_id = b.belong_id and employee_id=%s"
        row = select_one(sql, employee_id)
        tbl = ['employee_id', 'name', 'belong_id', 'mail_address', 'password', 'management', 'belong_name']
        errors = []
        user = {}
        if row is not None:
            for t, r in zip(tbl, row):
                user[t] = r
        return render_template('edit.html', errors=errors, user=user)
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
        sql = 'select employee_id from employee_tbl where mail_address=%s and password=%s'
        row = select_one(sql, mail_address, password)
        if row is None or row == employee_id:
            if len(management) != 0:
                management = management[0]
                sql = 'update employee_tbl set name=%s, belong_id=%s, mail_address=%s, \
                password=%s, management=%s where employee_id=%s'
            else:
                management = None
                sql = 'update employee_tbl set name=%s, belong_id=%s, mail_address=%s, \
                password=%s where employee_id=%s'
        else:
            return redirect(url_for('list'))
        change_tbl(sql, name, belong_id, mail_address, password, management, employee_id)
        return redirect(url_for('list'))
    else:
        return redirect(url_for('login'))

@app.route('/user/delete/<employee_id>', methods=['POST'])
def delete(employee_id):
    deleted_datetime = datetime.now().strftime('%Y-%m-%d')
    sql = 'update employee_tbl set deleted_datetime=%s where employee_id=%s'
    change_tbl(sql, deleted_datetime, employee_id)
    return redirect(url_for('list'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
