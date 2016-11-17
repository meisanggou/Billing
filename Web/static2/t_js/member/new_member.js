/**
 * Created by msg on 11/11/16.
 */

$(function(){
    $("#li_member").addClass("active open");
    $("#btn_save").click(function(){
        var validate_result = data_validate("div_member_info");
        show_msg(validate_result[1]);
        return true;
    });
});

