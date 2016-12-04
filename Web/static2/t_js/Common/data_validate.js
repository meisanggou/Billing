/**
 * Created by msg on 11/17/16.
 */

function data_validate(div_id){
    var data_div = $("#" + div_id);
    var input_data = new Object();
    var data_items = data_div.find("input,select,textarea");
    var input_len = data_items.length;
    for(var i=0;i<input_len;i++){
        var input_item = $(data_items[i]);
        var data_value = input_item.val();
        var param_name = input_item.attr("name");
        var data_required = input_item.attr("required");
        var data_rule = input_item.attr("data-validate");
        var validate_result = 0;
        if (data_value == "") {
            if (data_required != undefined) {
                input_item.select();
                validate_result = 1;
            }
            else{
                data_value = null;
            }
        }
        else if (data_rule != undefined) {
            var r = new RegExp(data_rule);
            if (!data_value.match(r)) {
                input_item.select();

            }
        }
        if(validate_result != 0){
            var data_rule_msg = input_item.attr("data-validate-msg");
            var mul_msg = data_rule_msg.split(";");
            if (data_rule_msg == undefined) {
                    return [false, "系统错误"];
            }
            if (mul_msg.length < 2) {
                return [false, "系统调用错误"]
            }
            var data_tip_name = mul_msg[0];
            if(validate_result == 1){
                return [false, "请输入" + data_tip_name]
            }
            else{
                return [false, mul_msg[1]];
            }
        }
        input_data[param_name] = data_value;
    }
    return [true, input_data]
}