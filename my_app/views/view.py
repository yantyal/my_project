from flask import redirect, url_for
from flask import session
from werkzeug.exceptions import HTTPException
import time, logging
from my_app.models import ( create_app, create_error_messages, formatter)


app = create_app()

DB_INFO = app.config['DB_INFO']
LOGFILE = app.config['LOGFILE']
UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

log_handler = logging.FileHandler(LOGFILE, encoding='utf-8')
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