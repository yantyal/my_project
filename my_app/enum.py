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