/**
 * Created by meisanggou on 2016/9/2.
 */

var max_hour = 0;
var max_owner = "";
var max_time = 0;
var book_num = 0;
var current_user = $("#current_user_name").val();

function timestamp_2_str(timestamp)
{
    var d = new Date(timestamp * 1000);
    var hour = d.getHours();
    var minute = d.getMinutes();
    if(hour > max_hour)
        max_hour = hour;
    if(minute < 10)
        minute = "0" + minute;
    return hour + ":" + minute;
}

//function ensure_right_time()
//{
//    var now_time = new Date();
//    var hour = now_time.getHours();
//    var minute = now_time.getMinutes();
//    $("#btn_add_task").unbind('click');
//    if((9<=hour && hour<=11 || 14<=hour && hour<=17) && 10 <= minute &&　minute<=20){
//        if(hour <= max_hour)
//        {
//            $("#btn_add_task").attr("disabled", "disabled");
//
//            if(max_owner == current_user){
//                $("#btn_add_task").text("已预约本时段");
//            }
//            else {
//                $("#btn_add_task").text("已有他人预约");
//            }
//        }
//        else if(book_num >= 2)
//        {
//            $("#btn_add_task").attr("disabled", "disabled");
//            $("#btn_add_task").text("今日已预约2次");
//        }
//        else {
//            $("#btn_add_task").removeAttr("disabled");
//            $("#btn_add_task").click(save_task);
//            $("#btn_add_task").text("预约");
//        }
//    }
//    else{
//        $("#btn_add_task").attr("disabled", "disabled");
//        $("#btn_add_task").text("非预约时段");
//    }
//    setTimeout(ensure_right_time, 30000);
//}

function save_task()
{
    $("#btn_add_task").attr("disabled", "disabled");
    var reason = $("#request_reaseon").val();
    var reason_desc = $("#request_reaseon_desc").val();
    var request_data = new Object();
    request_data["reason"] = reason;
    request_data["reason_desc"] = reason_desc;
    var url_task = $("#url_task_list").val();
    my_async_request(url_task, "POST", request_data, request_task_list);
}

function request_task_list_success(data)
{
    if(data.status == false){
        sweetAlert(data.data);
    }
    var today_task_list = data.data;
    Add_Task_Info();
    book_num = 0;
    for(var i=0;i<today_task_list.length;i++){
        var status_list = new Array();
        var status_s_list = today_task_list[i].status_info.split("|");
        var j = 0;
        for(;j<status_s_list.length;j++)
        {
            var status_item = status_s_list[j];
            status_list[j] = new Object();
            var time = parseInt(status_item.substr(0, status_item.length - 1));
            if(time > max_time){
                max_time = time;
                max_owner = today_task_list[i].user_name;
            }
            status_list[j].time = timestamp_2_str(time);
            if(status_item[status_item.length - 1] == "0"){
                status_list[j].result = false;
            }
            else{
                status_list[j].result = true;
            }
        }
        for(;j < 5; j++){
            status_list[j] = null;
        }
        if(today_task_list[i].user_name == current_user){
            book_num += 1;
        }
        today_task_list[i].status_list = status_list;
        Add_Task_Info(today_task_list[i]);
    }
    ensure_right_time();
}

function request_task_list(data)
{
    if(data==null || data.status==true) {
        var url_task_list = $("#url_task_list").val();
        my_async_request(url_task_list, "GET", null, request_task_list_success)
    }
    else
    {
        sweetAlert(data.data);
    }
}


$(function(){
    request_task_list();
});