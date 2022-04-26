import mysql.connector, json
from werkzeug.utils import secure_filename
import os

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
        cursor.execute(sql, [arg for arg in args if arg != '' and arg != '0'])
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
    with open('sql.json', 'r') as file:
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
    if belong_id != '0':
        sql_condition.append("2")
    return sql_condition

# SQL文を保存するためのtable
def issue_table(table_name):
    with open('table.json', 'r') as file:
        tables = json.load(file)
    table = []
    for index in tables[table_name]:
        table.extend(tables[table_name][index])
    return table

# エラーメッセージを配列で返すメソッド
def create_error_messages(error_name):
    with open('errors.json', 'r', encoding='utf-8') as file:
        errors = json.load(file)
    messages = []
    for index in errors[error_name]:
        messages.extend(errors[error_name][index])
    return messages

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])
def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, filename, app_config_UPLOAD_FOLDER):
    if file and allwed_file(filename):
        # 危険な文字を削除（サニタイズ処理）
        filename = secure_filename(filename)
        # ファイルの保存
        file.save(os.path.join(app_config_UPLOAD_FOLDER, filename))
    return filename