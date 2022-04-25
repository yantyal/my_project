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