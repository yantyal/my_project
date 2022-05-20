from flask import Blueprint, redirect, url_for
from flask import session
from datetime import datetime
from my_app.models import (change_tbl, issue_sql)
from my_app.view import DB_INFO

delete_bp = Blueprint('delete', __name__, url_prefix='/user', template_folder='my_app.templates')

# 削除(実際にはデータは削除しない)
@delete_bp.route('/delete/<employee_id>', methods=['POST'])
def delete(employee_id):
    if session['management'] != 'Y':
        return redirect(url_for('list.list'))

    deleted_datetime = datetime.now().strftime('%Y-%m-%d')
    sql = issue_sql('delete')
    change_tbl(DB_INFO, sql, deleted_datetime, employee_id)
    return redirect(url_for('list.list'))