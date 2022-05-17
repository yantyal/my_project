document.addEventListener("DOMContentLoaded", function(){
    // アップロード予定の画像を表示する
    document.getElementById('file').addEventListener('change', function (e) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("preview").setAttribute('src', e.target.result);
        }
        reader.readAsDataURL(e.target.files[0]);
        });
})