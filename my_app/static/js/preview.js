document.addEventListener("DOMContentLoaded", function(){
    // アップロード予定の画像を表示する
    document.getElementById('file').addEventListener('change', function (e) {
        var reader = new FileReader();
        reader.onload = function (e) {
            function is_check_file_data(){
                return  e.target.result.indexOf('image/') === 5;
            }
            if(is_check_file_data()){
                document.getElementById("preview").setAttribute('src', e.target.result);
                document.getElementById("error-message").innerText = ''
            }else{
                document.getElementById("preview").setAttribute('src', '/static/img/noimage.png');
                document.getElementById("error-message").innerText = '登録できないファイルが選択されました。'
            }
        }
        reader.readAsDataURL(e.target.files[0]);
        });
})