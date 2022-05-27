document.addEventListener("DOMContentLoaded", function(){
    // 編集画面で所属部署を選択状態にする
    var selects = document.getElementsByClassName("belong_id");
    var number = document.getElementById("user_belong_id").value;
    for(let i=0; i < selects.length; i++){
        selects[i].options[number].selected = true;
    }
})