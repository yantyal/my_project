document.addEventListener("DOMContentLoaded", function(){
    // 編集画面で所属部署を選択状態にする
    var select = document.getElementById("belong_id");
    var number = document.getElementById("user_belong_id").value;
    select.options[number].selected = true;
})