from flask import render_template, redirect, url_for, make_response
from flask import request, session
from werkzeug.exceptions import HTTPException
from datetime import datetime
import time, json, logging
from my_app.models import (check_error_in_session, check_success_in_session, create_app, create_error_messages, create_sql_condition, create_success_messages, create_users,
issue_table, save_file, select_one, select_all, change_tbl, issue_sql, create_hash, formatter)
from flask import Blueprint, render_template
from my_app.view import DB_INFO

login_bp = Blueprint('login', __name__, url_prefix='/login', template_folder='my_app.templates')

# ログイン
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            return redirect(url_for('list.list'))

        user_info = request.cookies.get('user_info')
        if user_info is None:
            check_error_in_session(session, 1)
            return render_template('login.html')

        # クッキーにユーザー情報があればログイン
        user_info = json.loads(user_info)
        mail_address = user_info['mail_address']
        password = user_info['password']
        sql = issue_sql('login')
        row = select_one(DB_INFO, sql, mail_address, password)
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
            return redirect(url_for('list.list'))
        else:
            return render_template('login.html')

    if request.method == 'POST':
        mail_address = request.form['mail_address']
        password = create_hash(request.form['password'])
        check_cookie = request.form.getlist('check_cookie')
        if len(check_cookie) != 0:
            check_cookie = check_cookie[0]
        sql = issue_sql('login')
        row = select_one(DB_INFO, sql, mail_address, password)
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
        response = make_response(redirect(url_for('list.list')))
        user_info = {'mail_address': mail_address, 'password': password}
        response.set_cookie("user_info", value=json.dumps(user_info), expires=expires)
        return response
    else:
        return redirect(url_for('list.list'))