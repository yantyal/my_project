from flask import Flask
import mysql.connector, json
from datetime import timedelta
from werkzeug.utils import secure_filename
import os, hashlib, time


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_envvar('APPLICATION_SETTINGS')
    app.permanent_session_lifetime = timedelta(minutes=30) # セッションの生存時間は30分
    return app


def connect_db():
    conn = mysql.connector.connect(
        host = 'localhost',
        user = 'user21',
        passwd = 'user21(PASS)',
        db = 'employee',
        auth_plugin="mysql_native_password"
    )
    return conn

# select文を一行返すメソッド
def select_one(sql, *args):
    row = None
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, [arg for arg in args if arg is not None ])
        row = cursor.fetchone()
    except(mysql.connector.errors.ProgrammingError) as e:
            print(e)
    finally:
        cursor.close()
        conn.close()
    return row

# select文を複数行返すメソッド
def select_all(sql, *args):
    rows = None
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, [arg for arg in args if arg != ''])
        rows = cursor.fetchall()
    except(mysql.connector.errors.ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return rows

# insert文、delete文、update文を実行するメソッド
def change_tbl(sql, *args):
    conn = connect_db()
    cursor = conn.cursor()
    print([arg for arg in args if arg is not None])
    try:
        cursor.execute(sql, [arg for arg in args if arg is not None])
        conn.commit()
    except(mysql.connector.errors.ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

# SQL文を発行するメソッド、条件によりSQL文が変わる場合は配列を渡す
def issue_sql(sql_name, dict_list=[]):
    with open('json/sql.json', 'r') as file:
        sqls = json.load(file)
    sql = ''
    for index in sqls[sql_name]:
        if type(sqls[sql_name][index]) == dict:
            for dl in dict_list:
                sql += sqls[sql_name][index][dl]
        else:
            sql += sqls[sql_name][index]
    return sql

def create_sql_condition(employee_id, name, belong_id):
    sql_condition = []
    if employee_id:
        sql_condition.append("0")
    if name:
        sql_condition.append("1")
    if belong_id != '':
        sql_condition.append("2")
    return sql_condition

# SQL文を保存するためのtable
def issue_table(table_name):
    with open('json/table.json', 'r') as file:
        tables = json.load(file)
    table = []
    for index in tables[table_name]:
        table.extend(tables[table_name][index])
    return table

# エラーメッセージを配列で返すメソッド
def create_error_messages(error_name):
    with open('json/errors.json', 'r', encoding='utf-8') as file:
        errors = json.load(file)
    messages = []
    for index in errors[error_name]:
        messages.extend(errors[error_name][index])
    return messages

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif','jpeg'])
def allowed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, filename, app_config_UPLOAD_FOLDER):
    if file and allowed_file(filename):
        # 危険な文字を削除（サニタイズ処理）
        filename = secure_filename(filename)
        # ファイルの保存
        file.save(os.path.join(app_config_UPLOAD_FOLDER, filename))
    return filename

def create_hash(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def create_users(table, rows):
    users = []
    for row in rows:
        user = {}
        for t, r in zip(table, row):
            user[t] = r
        users.append(user)
    return users

# meantimeはセッションに残すエラー文の生存時間
def check_error_in_session(session, meantime):
    end = time.time()
    if 'start' in session:
        if end - session['start'] >= meantime:
            session.pop('errors', None)
            session.pop('start', None)

# 成功メッセージを配列で返すメソッド
def create_success_messages(success_name):
    with open('json/success.json', 'r', encoding='utf-8') as file:
        success = json.load(file)
    messages = []
    for index in success[success_name]:
        messages.extend(success[success_name][index])
    return messages

# meantimeはセッションに残す成功文の生存時間
def check_success_in_session(session, meantime):
    end = time.time()
    if 'success_start' in session:
        if end - session['success_start'] >= meantime:
            session.pop('success', None)
            session.pop('success_start', None)