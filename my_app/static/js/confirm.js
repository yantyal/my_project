var deletes = document.getElementsByClassName('delete');
for(let i = 0; i < deletes.length; i++){
    deletes[i].addEventListener('click', function(e){
        if(!confirm('削除しますか?')){
            e.preventDefault();
        }
    });
}