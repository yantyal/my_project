import mysql.connector

#DB接続情報
def conn_db():
      conn = mysql.connector.connect(
              host = 'localhost',      #localhostでもOK
              user = 'user21',
              passwd = 'user21(PASS)',
              db = 'employee'
      )
      return conn

# name = '木村'
# belong_id = 5
# mail_address = 'kimura@example.com'
# password = 'kimurapass'
# #本体
# sql = f'select * from employee_tbl where mail_address=\'{mail_address}\'\
#       and password=\'{password}\''
# try:
#       conn = conn_db()              #ここでDBに接続
#       cursor = conn.cursor()       #カーソルを取得
#       cursor.execute(sql)           #selectを投げる
#       rows = cursor.fetchall()      #selectの結果を全件タプルに格納
# except(mysql.connector.errors.ProgrammingError) as e:
#       print('エラーだぜ')
#       print(e)


# if len(rows) == 0:
#       sql2 = f'insert into employee_tbl(name, belong_id, mail_address, password)\
#                   values(\'{name}\', {belong_id}, \'{mail_address}\', \'{password}\' )'
#       print(sql2)
#       try:
#             conn = conn_db()              #ここでDBに接続
#             cursor = conn.cursor()       #カーソルを取得
#             cursor.execute(sql2)           #selectを投げる
#             conn.commit()
#             # rows = cursor.fetchall()      #selectの結果を全件タプルに格納
#       except(mysql.connector.errors.ProgrammingError) as e:
#             print('エラーだぜ')
#             print(e)
# else:
#       print('登録できないメールアドレスと\nパスワードです')

# print('select結果だぜ')
# tbl = ['emp_id', 'name', 'belong_id', 'email', 'password', 'management',
#             'deleted_datetime', 'image_file_path']
# user = {}
# for row in rows:
#     for r in row:
#         print(r)


def change_tbl(sql):
      try:
            conn = conn_db()              #ここでDBに接続
            cursor = conn.cursor()       #カーソルを取得
            cursor.execute(sql)           #selectを投げる
            conn.commit()
            # rows = cursor.fetchall()      #selectの結果を全件タプルに格納
      except(mysql.connector.errors.ProgrammingError) as e:
            print(e)
employee_id = 12

sql3 = f'delete from employee_tbl where employee_id=\'{employee_id}\''
print(sql3)
change_tbl(sql3)


