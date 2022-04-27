function delete_check(){
    if(window.confirm('削除しますか？')){
        window.alert('削除を受けつけました');
        return true;
    }
    else{
        window.alert('キャンセルされました');
        return false;
    }
}

function add_check(){
    if(window.confirm('ユーザー登録しますか？')){
        window.alert('登録を受けつけました');
        return true;
    }
    else{
        window.alert('キャンセルされました');
        return false;
    }
}

function edit_check(){
    if(window.confirm('登録情報を変更しますか？')){
        window.alert('変更を受けつけました');
        return true;
    }
    else{
        window.alert('キャンセルされました');
        return false;
    }
}

function sort_clear(){
    location.href = "./list";
}