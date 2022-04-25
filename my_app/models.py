import mysql.connector

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
        cursor.execute(sql, [arg for arg in args if arg is not None ]) # なぜかlist(args)がエラーになる
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
        cursor.execute(sql, [arg for arg in args if arg != '' and arg != '0']) # なぜかlist(args)がエラーになる
        rows = cursor.fetchall()
    except(mysql.connector.errors.ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
    return rows

# insert文, delete文を実行するメソッド
# update文はまだ試していない
def change_tbl(sql, *args):
    conn = connect_db()
    cursor = conn.cursor()
    print([arg for arg in args if arg is not None])
    try:
        cursor.execute(sql, [arg for arg in args if arg is not None]) # なぜかlist(args)がエラーになる
        conn.commit()
    except(mysql.connector.errors.ProgrammingError) as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
