// 編集画面で所属部署を選択状態にする
document.addEventListener("DOMContentLoaded", function(){
    var select = document.getElementById("belong_id");
    var number = document.getElementById("user_belong_id").value
    select.options[number].selected = true
})

// アップロード予定の画像を表示する
document.getElementById('file').addEventListener('change', function (e) {
    var reader = new FileReader();
    reader.onload = function (e) {
        document.getElementById("preview").setAttribute('src', e.target.result);
    }
    reader.readAsDataURL(e.target.files[0]);
    });

function password_mask(obj) {
    console.log(obj)
    var txtPass = document.getElementById(('emp_id' + obj));
    var btnEye = document.getElementById(('btn_emp_id' + obj));
    if (txtPass.type === "text") {
        txtPass.type = "password";
        console.log(btnEye.className)
        btnEye.className = "fa fa-eye";
    } else {
        txtPass.type = "text";
        console.log(btnEye.className)
        btnEye.className = "fa fa-eye-slash";
    }
}
function password_mask(){
    var txtPass = document.getElementById('login');
    var btnEye = document.getElementById('btn_login');
    if (txtPass.type === "text") {
        txtPass.type = "password";
        btnEye.className = "fa fa-eye";
    } else {
        txtPass.type = "text";
        btnEye.className = "fa fa-eye-slash";
    }
}