from flask import render_template, redirect, url_for, make_response
from flask import request, session, current_app
from datetime import datetime
import json
from my_app.enum import (transition_redirect_target, transition_render_template_target,
Login_user_info, sql_name, table_name)
from my_app.models import (check_error_in_session,issue_table, register_messages_in_session,
select_one, issue_sql, create_hash)
from flask import Blueprint, render_template

login_bp = Blueprint('login', __name__, url_prefix='/login', template_folder='my_app.templates')

# ログイン前処理
@login_bp.before_request
def user_load():
    if request.method == 'GET':
        if Login_user_info.NAME.value in session:
            return redirect(url_for(transition_redirect_target.LIST.value))


# ログイン
@login_bp.route('/', methods=['GET', 'POST'])
def login():
    DB_INFO = current_app.config['DB_INFO']

    if request.method == 'GET':
        user_info = request.cookies.get('user_info')
        if user_info is None:
            check_error_in_session(session)
            return render_template(transition_render_template_target.LOGIN.value)

        # クッキーにユーザー情報があればログイン
        user_info = json.loads(user_info)
        mail_address = user_info['mail_address']
        password = user_info['password']
        sql = issue_sql(sql_name.LOGIN.value)
        row = select_one(DB_INFO, sql, mail_address, password)
        table = issue_table(table_name.LOGIN.value)
        current_app.logger.info(sql)

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
            return redirect(url_for(transition_redirect_target.LIST.value))
        else:
            return render_template(transition_render_template_target.LOGIN.value)

    if request.method == 'POST':
        mail_address = request.form['mail_address']
        password = create_hash(request.form['password'])
        check_cookie = request.form.getlist('check_cookie')
        if len(check_cookie) != 0:
            check_cookie = check_cookie[0]
        sql = issue_sql(sql_name.LOGIN.value)
        row = select_one(DB_INFO, sql, mail_address, password)
        table = issue_table(table_name.LOGIN.value)
        current_app.logger.info(sql)

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
        register_messages_in_session(session, 'errors', 'login')
        current_app.logger.info(session['errors'])
        return redirect(url_for(transition_redirect_target.LOGIN.value))

    if check_cookie == 'ok':
        max_age = 30 # クッキーの生存時間は30秒
        expires = int(datetime.now().timestamp()) + max_age
        response = make_response(redirect(url_for(transition_redirect_target.LIST.value)))
        user_info = {'mail_address': mail_address, 'password': password}
        response.set_cookie("user_info", value=json.dumps(user_info), expires=expires)
        return response
    else:
        return redirect(url_for(transition_redirect_target.LIST.value))