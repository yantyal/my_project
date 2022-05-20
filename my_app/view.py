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
from my_app.views.edit import edit_bp
app.register_blueprint(edit_bp)
from my_app.views.delete import delete_bp
app.register_blueprint(delete_bp)

# インデックス
@app.route('/')
def index():
    app.logger.info('From Index To Login.')
    return redirect(url_for('login.login'))


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