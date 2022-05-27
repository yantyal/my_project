document.addEventListener("DOMContentLoaded", function(){
    // アップロード予定の画像を表示する
    var files = document.getElementsByClassName('file')
    for(let i=0; i < files.length; i++){
        files[i].addEventListener('change', function (e) {
            var reader = new FileReader();
            reader.onload = function (e) {
                function is_check_file_data(){
                    return  e.target.result.indexOf('image/') === 5;
                }
                if(is_check_file_data()){
                    for(let j=0; j<files.length; j++){
                        files[j].files = files[i].files
                        document.getElementsByClassName("preview")[j].setAttribute('src', e.target.result);
                        document.getElementsByClassName("error-message")[j].innerText = ''
                    }
                }else{
                    for(let j=0; j<files.length; j++){
                        files[j].files = files[i].files
                        document.getElementsByClassName("preview")[j].setAttribute('src', '/static/img/noimage.png');
                        document.getElementsByClassName("error-message")[j].innerText = '登録できないファイルが選択されました。'
                    }
                }
            }
            reader.readAsDataURL(e.target.files[0]);
        });
    }
})