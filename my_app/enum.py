from enum import Enum


# render_templateにより画面遷移先HTML
class transition_render_template_target(Enum):
    LOGIN = 'login.html'
    LIST = 'list.html'
    ADD = 'add.html'
    EDIT = 'edit.html'

# リダイレクトによる画面遷移先モジュールのメソッド
class transition_redirect_target(Enum):
    LOGIN = 'login.login'
    LIST = 'list.list'
    ADD = 'add.add'
    EDIT = 'edit.edit'

# 新規登録時の条件分岐
class Add_sql_condition(Enum):
    NOT_EXIST_FILENAME_AND_MANAGEMENT = '0'
    EXIST_MANAGEMENT = '1'
    EXIST_FILENAME = '2'
    EXIST_FILENAME_AND_MANAGEMENT = '3'

# ログイン時にセッションに残すユーザー情報
class Login_user_info(Enum):
    EMPLOYEE_ID = 'employee_id'
    NAME = 'name'
    DELETED_DATETIME = 'deleted_datetime'
    MANAGEMENT = 'management'

# 呼び出されるSQLの名前
class sql_name(Enum):
    LOGIN = 'login'
    LIST = 'list'
    SORT = 'sort'
    ADD_CHECK = 'add_check'
    ADD = 'add'
    EDIT_USER_INFO = 'edit_user_info'
    EDIT_CHECK = 'edit_check'
    EDIT = 'edit'
    CHANGE_PASSWORD = 'change_password'
    DELETE = 'delete'

# 呼び出されるテーブルの名前
class table_name(Enum):
    LOGIN = 'login'
    LIST = 'list'
    EDIT = 'edit'