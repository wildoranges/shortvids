function postsub(){
    const url = "../subscribe/";
    let csrf = "{{ csrf_token }}";
    const form_data = new FormData();
    form_data.append("csrfmiddlewaretoken", csrf);
    form_data.append("from_user", "{{ request.session.user_id }}");
    form_data.append("to_user", "{{video.uploader_id.user_id}}");
    const request = new XMLHttpRequest();
    request.open("POST", url, true);
    //request.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    request.send(form_data);
    let cnt = 0;
    request.onreadystatechange = function() {
        if(request.readyState == 4 && request.status == 200){
            alert("订阅成功");
        }else if(request.readyState == 4){
            cnt ++;
            console.log(cnt);
            alert("订阅失败，请稍后再试");
        }
    }
}