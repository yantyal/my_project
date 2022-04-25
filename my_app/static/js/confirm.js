function delete_check(){
    if(window.confirm('削除しますか？')){
        window.alert('削除されました');
        return true;
    }
    else{
        window.alert('キャンセルされました');
        return false;
    }
}

function add_check(){
    if(window.confirm('ユーザー登録しますか？')){
        window.alert('登録されました');
        return true;
    }
    else{
        window.alert('キャンセルされました');
        return false;
    }
}

function edit_check(){
    if(window.confirm('登録情報を変更しますか？')){
        window.alert('変更されました');
        return true;
    }
    else{
        window.alert('キャンセルされました');
        return false;
    }
}