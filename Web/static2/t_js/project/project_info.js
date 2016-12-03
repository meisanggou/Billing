/**
 * Created by msg on 11/9/16.
 */

function new_project(){
    var request_url = location.href;
    var project_name = $("#project_name").val();
    var project_desc = $("#project_desc").val();
    var request_data = {"project_name": project_name, "project_desc": project_desc};
    my_async_request(request_url, "POST", request_data, null)
}

function update_project(){
    var request_url = location.href;
    var project_name = $("#project_name").val();
    var project_desc = $("#project_desc").val();
    var request_data = {"project_name": project_name, "project_desc": project_desc};
    my_async_request(request_url, "PUT", request_data, null);
}

function init_project(data){
    if(data != null){
        $("#project_name").val(data["project_name"]);
        $("#project_name").attr("disabled", "disabled");
        $("#project_desc").val(data["project_desc"]);
        $("#btn_op_project").text("更新项目");
        $("#btn_op_project").click(update_project);
    }
    else{
        $("#btn_op_project").click(new_project);
    }
}


$(function(){
    $("#li_project_info").addClass("active open");
    var request_url = location.href;
    my_async_request(request_url, "GET", null, init_project)
});