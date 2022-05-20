from flask import redirect, url_for
from flask import session
from werkzeug.exceptions import HTTPException
import time, json, logging
from my_app.models import ( create_app, create_error_messages, formatter)


app = create_app()

DB_INFO = app.config['DB_INFO']
LOGFILE = app.config['LOGFILE']
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

log_handler = logging.FileHandler(LOGFILE)
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)


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
    return redirect(url_for('list.list'))


# 汎用的なエラーハンドラー
@app.errorhandler(HTTPException)
def error_handler(error):
    session['errors'] = create_error_messages('error')
    session['start'] = time.time()
    if 'name' not in session:
        return redirect(url_for('login.login'))
    return redirect(url_for('list.list'))