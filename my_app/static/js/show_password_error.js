// パスワードの更新に失敗した場合、モーダルを再表示
// エラーメッセージを表示
document.addEventListener("DOMContentLoaded", function(){
    var error_change_password = document.getElementById('error_change_password');
    var error_change_password_value = "";
    if(error_change_password != null){
        error_change_password_value = error_change_password.value;
    }
    if(error_change_password_value != ''){
        new bootstrap.Modal('#modal').show();
        document.getElementById('password-error-message').innerHTML = '<p class="text-danger ms-2 my-auto" id="error-message">※パスワードの更新に失敗しました。</p>';
    }
    var show_modals = document.getElementsByClassName('show-modal');
    for(let i = 0; i < show_modals.length; i++){
        show_modals[i].addEventListener('click', function(e){
            document.getElementById('password-error-message').innerHTML = '';
        })
    }
})