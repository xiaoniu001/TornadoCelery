$(document).ready(function(){

//    获取cookie
    function getCookie(name) {
        var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
        return r ? r[1] : undefined;
    }


    $("#submit").click(function(){
        $('#submit').addClass('active');
        _xsrf = getCookie("_xsrf");
        var username = $("#username").val();
        var password = $("#password").val();
        var dwno = $("#dwno").val();
        var project_code = parent.$("#project_code").val();
        var function_code = parent.$("#function_code").val();
        console.log("用户名密码", username, password);
        $.ajax({
            type: "POST",
            url:'/login',
            data:{"project_code":project_code, "function_code":function_code, "username": username,
            "password": password, "_xsrf": _xsrf, "dwno": dwno},
            dataType:'json',
            success:function(data){
                console.log(data);
                $('#submit').removeClass('active');
                if(data.success){
                    var index = parent.layer.getFrameIndex(window.name);
                    parent.layer.close(index);
                    parent.window.location="/alarm";
                }else{
                    $("#message").html(data.message)
                }
            }
        })
    });
});