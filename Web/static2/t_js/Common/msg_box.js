/**
 * Created by msg on 11/17/16.
 */
function show_msg(info,type,t){
    var winObj = null;
    var timeout = 3000;
    if(t || t===0){
        timeout = t;
    }
    winObj = $("#winAlert");
    winObj.find("p").html(info);

    winObj.removeClass("hide");
    winObj.addClass("in");

    if(timeout>0){
        setTimeout(function(){
            winObj.removeClass("in");winObj.addClass("hide");
        }, timeout);
    }
}
function msgboxClose(){
    $("#winAlert").addClass("hide");
    $("#winAlert").removeClass("in");
}

$(function(){
        $("#btn_close_msg_box").click(msgboxClose);
    }
);