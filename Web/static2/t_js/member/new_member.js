/**
 * Created by msg on 11/11/16.
 */

$(function(){
    $("#li_add_member").addClass("active open");
    $("#btn_save").click(function() {
        var validate_result = data_validate("div_member_info");
        if (validate_result[0] == false) {
            show_msg(validate_result[1]);
            return false;
        }
        var input_data = validate_result[1];
        my_async_request("/member/", "POST", input_data);
        return true;
    });
});


$(document).ready(function(){
	Bind_Date($(".date"), "left", 1);
});

