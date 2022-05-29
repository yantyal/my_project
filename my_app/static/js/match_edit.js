document.addEventListener("DOMContentLoaded", function(){
    // 名前を一致させる
    names = document.getElementsByClassName('name')
    names[1].value = names[0].value;
    names[0].addEventListener('change', function(){
        names[1].value = names[0].value;
    })
    names[1].addEventListener('change', function(){
        names[0].value = names[1].value;
    })
    // メールアドレスを一致させる
    emails = document.getElementsByClassName('email');
    emails[1].value = emails[0].value;
    emails[0].addEventListener('change', function(){
        emails[1].value = emails[0].value;
    })
    emails[1].addEventListener('change', function(){
        emails[0].value = emails[1].value;
    })
    // プレビューの画像を一致させる
    previews = document.getElementsByClassName('preview')
    previews[1].src = previews[0].src;
    // 所属先を一致させる
    belong_ids = document.getElementsByClassName('belong_id')
    belong_ids[1].value = belong_ids[0].value
    belong_ids[0].addEventListener('change', function(){
        for(let i=0; i < belong_ids[1].options.length; i++){
            if(belong_ids[0].options[i].selected){
                belong_ids[1].options[i].selected = true
            }
        }
    })
    belong_ids[1].addEventListener('change', function(){
        for(let i=0; i < belong_ids[1].options.length; i++){
            if(belong_ids[1].options[i].selected){
                belong_ids[0].options[i].selected = true
            }
        }
    })
    // 管理者権限を一致させる
    managements = document.getElementsByClassName('management')
    if(managements[0].checked){
            managements[1].checked = true
    }else{
        managements[1].checked = false
    }
    managements[0].addEventListener('change', function(){
        if(managements[0].checked){
            managements[1].checked = true
        }else{
            managements[1].checked = false
        }
    })
    managements[1].addEventListener('change', function(){
        if(managements[1].checked){
            managements[0].checked = true
        }else{
            managements[0].checked = false
        }
    })
    //  パスワードを一致させる
    passwords = document.getElementsByClassName('add-password');
    if (passwords != null){
        passwords[1].value = passwords[0].value;
        passwords[0].addEventListener('change', function(){
            passwords[1].value = passwords[0].value;
        })
        passwords[1].addEventListener('change', function(){
            passwords[0].value = passwords[1].value;
        })
    }
})