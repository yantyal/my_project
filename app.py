from flask import Flask, render_template, redirect, url_for
from flask import request, session
from datetime import timedelta
import mysql.connector

app = Flask(__name__)
app.secret_key = 'abcdefghijklmn'
app.permanent_session_lifetime = timedelta(minutes=3) # sessionの生存時間

def connect_db():
    conn = mysql.connector.connect(
            host = 'localhost',
            user = 'user21',
            passwd = 'user21(PASS)',
            db = 'employee'
    )
    return conn

# select文を一行返すメソッド
def select_one(sql):
    row = None
    try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
    except(mysql.connector.errors.ProgrammingError) as e:
            print(e)
    return row

# select文を複数行返すメソッド
def select_all(sql):
    rows = None
    try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
    except(mysql.connector.errors.ProgrammingError) as e:
        print(e)
    return rows

# insert文, delete文を実行するメソッド
# update文はまだ試していない
def change_tbl(sql):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    except(mysql.connector.errors.ProgrammingError) as e:
        print(e)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail_address = request.form['mail_address']
        password = request.form['password']
        sql = f'select employee_id, name, deleted_datetime, management \
            from employee_tbl where mail_address=\'{mail_address}\'\
            and password=\'{password}\''
        print(sql)
        row = select_one(sql)
        print(row)
        tbl = ['employee_id', 'name', 'deleted_datetime', 'management']
        errors = ['ログインに失敗しました。',
                'メールアドレスとパスワードをご確認ください。']
        if row is not None:
            for t, r in zip(tbl, row):
                session[t] = r
                if t == 'deleted_datetime' and r is not None:
                    session.clear()
                    return render_template('login.html', errors=errors)
            return redirect(url_for('list'))
        else:
            #TODO errors送ったあとリロードするとフォームを再送してしまうところの改善
            # トークンを利用する
            return render_template('login.html', errors=errors)
    else:
        if 'name' in session:
            return redirect(url_for('list'))
        else:
            return render_template('login.html')

@app.route('/user/list', methods=['GET','POST'])
def list():
    if 'name' in session:
        sql = ''
        if request.method == 'GET':
            sql = '''
                select e.employee_id, e.name, e.mail_address, e.password,
                coalesce(e.management, ''), coalesce(e.deleted_datetime, ''), 
                coalesce(e.image_file_path, ''), coalesce(e.belong_id, ''), b.belong_name 
                from employee_tbl as e inner join belong_master_tbl as b  
                where e.belong_id = b.belong_id  
                order by management desc, employee_id
                '''
        else:
            emp_id = request.form['emp_id']
            name = request.form['name']
            belong_id = request.form['belong_id']
            prepared_sql = ''
            if emp_id:
                prepared_sql += ' and e.employee_id=' + emp_id 
            if name:
                prepared_sql += ' and e.name like \'%' + name + '%\''
            if belong_id != '0':
                prepared_sql += ' and e.belong_id=' + belong_id + ''
            sql = '''
                select e.employee_id, e.name, e.mail_address, e.password,
                coalesce(e.management, ''), coalesce(e.deleted_datetime, ''), 
                coalesce(e.image_file_path, ''), coalesce(e.belong_id, ''), b.belong_name 
                from employee_tbl as e inner join belong_master_tbl as b  
                where e.belong_id = b.belong_id 
                ''' \
                + prepared_sql + ' order by management desc, employee_id'                
        rows = select_all(sql)
        tbl = ['employee_id', 'name', 'mail_address', 'password', 'management',
                'deleted_datetime', 'image_file_path','belong_id', 'belong_name']
        users = []
        errors = []
        if rows is not None:
            if len(rows) == 0:
                errors = ['リストに存在しません']
                return render_template('list.html', errors=errors, users=users)
            for row in rows:
                user = {}
                for t, r in zip(tbl, row):
                    user[t] = r
                users.append(user)
        else:
            errors = ['リストの取得に失敗しました。']
            return render_template('list.html', errors=errors, users=users)
        return render_template('list.html', errors=errors, users=users) 
    else:
        return redirect(url_for('login'))

@app.route('/user/add', methods=['GET', 'POST'])
def add():
    if 'name' in session:
        if request.method == 'POST':
            name = request.form['name']
            belong_id = request.form['belong_id']
            mail_address = request.form['mail_address']
            password = request.form['password']
            management = request.form.getlist('management')
            if len(management) != 0:
                management = management[0]
            sql = f'select * from employee_tbl where mail_address=\'{mail_address}\'\
                    and password=\'{password}\''
            row = select_one(sql)
            if row is None:
                if management == 'Y':
                    sql = f'insert into employee_tbl(name, belong_id, mail_address, password, management)\
                        values(\'{name}\', {belong_id}, \'{mail_address}\', \'{password}\' , \'{management}\')'
                else:
                        sql = f'insert into employee_tbl(name, belong_id, mail_address, password)\
                        values(\'{name}\', {belong_id}, \'{mail_address}\', \'{password}\' )'
                change_tbl(sql)
            else:
                errors = ['登録できないメールアドレスと',
                        'パスワードです']
                return render_template('add.html', errors=errors)
            return redirect(url_for('list'))
        else:
            errors = []
            return render_template('add.html',errors=errors)
    else:
        return redirect(url_for('login'))

@app.route('/user/edit/<employee_id>', methods=['GET', 'POST'])
def edit(employee_id):
    if 'name' in session:
        sql = f'select e.name, e.belong_id, e.mail_address, e.password, e.management, \
            b.belong_name\
            from employee_tbl as e inner join belong_master_tbl as b \
            where e.belong_id = b.belong_id and employee_id={employee_id}'
        print(sql)
        row = select_one(sql)
        tbl = ['name', 'belong_id', 'mail_address', 'password', 'management', 'belong_name']
        user = {}
        if row is not None:
            for t, r in zip(tbl, row):
                user[t] = r
        print(user)
        return render_template('edit.html', user=user)
    else:
        return redirect(url_for('login'))

@app.route('/user/result', methods=['POST'])
def edit_result():
    if 'name' in session:
        name = request.form['name']
        belong_id = request.form['belong_id']
        mail_address = request.form['mail_address']
        password = request.form['password']
        management = request.form.getlist('management')
        return redirect(url_for('list'))
    else:
        return redirect(url_for('login'))
# name = request.form['name']
#     belong_id = request.form['belong_id']
#     mail_address = request.form['mail_address']
#     password = request.form['password']
#     sql = f'update employee_tbl set name=\' {name} \',\
#         belong_id=\' {belong_id} \', mail_address=\' {mail_address} \
#         password=\' {password} \' where employee_id=\' {employee_id} \''
#     change_tbl(sql)

@app.route('/user/delete/<employee_id>', methods=['POST'])
def delete(employee_id):
    # TODO delete文を実行するのではなく、deleted_datetimeに削除時の時間を追加
    sql = f'delete from employee_tbl where employee_id=\'{employee_id}\''
    change_tbl(sql)
    return redirect(url_for('list'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


