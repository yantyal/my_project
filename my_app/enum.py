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