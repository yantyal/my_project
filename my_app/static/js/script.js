document.addEventListener("DOMContentLoaded", function(){
    // パスワードのマスク表示
    var passwords = document.getElementsByClassName('password');
    var btn_view_passwords = document.getElementsByClassName('btn-view-password');
    for(let i = 0; i < btn_view_passwords.length; i++){
        btn_view_passwords[i].addEventListener('click', function(e){
            e.preventDefault();
            if(passwords[i].type === 'password') {
                passwords[i].type = 'text';
                btn_view_passwords[i].innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-slash-fill text-muted" viewBox="0 0 16 16">'
                                                    +'<path d="m10.79 12.912-1.614-1.615a3.5 3.5 0 0 1-4.474-4.474l-2.06-2.06C.938 6.278 0 8 0 8s3 5.5 8 5.5a7.029 7.029 0 0 0 2.79-.588zM5.21 3.088A7.028 7.028 0 0 1 8 2.5c5 0 8 5.5 8 5.5s-.939 1.721-2.641 3.238l-2.062-2.062a3.5 3.5 0 0 0-4.474-4.474L5.21 3.089z"/>'
                                                    +'<path d="M5.525 7.646a2.5 2.5 0 0 0 2.829 2.829l-2.83-2.829zm4.95.708-2.829-2.83a2.5 2.5 0 0 1 2.829 2.829zm3.171 6-12-12 .708-.708 12 12-.708.708z"/>'
                                                    +'</svg>';
            } else {
                passwords[i].type = 'password';
                btn_view_passwords[i].innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye text-muted" viewBox="0 0 16 16">'
                                                    +'<path d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"/>'
                                                    +'<path d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"/>'
                                                    +'</svg>';
            }
        });
    }

    // 編集画面で所属部署を選択状態にする
    var select = document.getElementById("belong_id");
    var number = document.getElementById("user_belong_id").value;
    select.options[number].selected = true;

    // アップロード予定の画像を表示する
    document.getElementById('file').addEventListener('change', function (e) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("preview").setAttribute('src', e.target.result);
        }
        reader.readAsDataURL(e.target.files[0]);
        });
})