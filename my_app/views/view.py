from flask import redirect, url_for
from flask import session
from my_app.enum import transition_redirect_target
from my_app.models import (create_app, formatter)
import logging


app = create_app()

LOGFILE = app.config['LOGFILE']

log_handler = logging.FileHandler(LOGFILE, encoding='utf-8')
log_handler.setFormatter(formatter)
app.logger.addHandler(log_handler)


# インデックス
@app.route('/')
def index():
    app.logger.info('From Index To Login.')
    return redirect(url_for(transition_redirect_target.LOGIN.value))


# ログアウト
@app.route('/logout')
def logout():
    formatter.set_employee_id(session)
    app.logger.info('Logout.')
    session.clear()
    return redirect(url_for(transition_redirect_target.LOGIN.value))