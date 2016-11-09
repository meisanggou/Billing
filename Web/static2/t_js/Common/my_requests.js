/**
 * Created by msg on 5/21/16.
 */

function request_error(xhr){
    var res = "状态码：" + xhr.status + "\n";
    res += "返回值：" + xhr.statusText + "";
    console.info(res);
    console.info(xhr);
    if(xhr.status === 301 || xhr.status === 302){
        swal({
                title: xhr.responseText,
                text: "是否重新登录",
                type: "warning",
                showCancelButton: true,
                confirmButtonColor: '#DD6B55',
                confirmButtonText: '重新登录',
                cancelButtonText: "取消",
                closeOnConfirm: true,
                closeOnCancel: true
            },
            function(isConfirm){
                if (isConfirm){
                    location.reload(true);
                }
            }
        );
    }
    else{
        sweetAlert(xhr.statusText);
    }
}


function my_request(request_url, request_method, body_param, request_success){
    if(request_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: request_url,
        method: request_method,
        contentType: "application/json",
        dataType: "json",
        data: body_param,
        async:false,
        success:function(data){
            if(data.status == false){
                sweetAlert(data.data);
            }
            else if("location" in data){
                location.href = data.location;
            }
            else if(request_success == null){
                sweetAlert(data.data);
            }
            else{
                request_success(data.data);
            }
        },
        error:request_error
    });
}

function my_async_request(request_url, request_method, body_param, request_success){
    if(request_method != "GET"){
        body_param = JSON.stringify(body_param)
    }
    $.ajax({
        url: request_url,
        method: request_method,
        contentType: "application/json",
        dataType: "json",
        data: body_param,
        success:function(data){
            if(data.status == false){
                sweetAlert(data.data);
            }
            else if("location" in data){
                location.href = data.location;
            }
            else if(request_success == null){
                sweetAlert(data.data);
            }
            else{
                request_success(data.data);
            }
        },
        error:request_error
    });
}
