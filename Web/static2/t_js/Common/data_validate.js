/**
 * Created by msg on 11/17/16.
 */

function data_validate(div_id){
    var data_div = $("#" + div_id);
    var mul_input_el = data_div.find("input");
    var input_len = mul_input_el.length;
    for(var i=0;i<input_len;i++){
        var input_item = $(mul_input_el[i]);
        console.info(input_item);
        var data_rule = input_item.attr("data-validate");
        var data_rule_msg = input_item.attr("data-validate-msg");
        if(data_rule_msg == undefined){
            return [false, "系统错误"];
        }
        var mul_msg = data_rule_msg.split(";");
        if(mul_msg.length < 2){
            return [false, "系统调用错误"]
        }
        var data_tip_name = mul_msg[0];
        var data_value = input_item.val();
        var data_required = input_item.attr("required");
        if(data_value == "") {
            if (data_required != undefined) {
                input_item.select();
                return [false, "请输入" + data_tip_name]
            }
        }
        else{
            console.info(data_rule);
            var r = new RegExp(data_rule);
            if(!data_value.match(r)){
                input_item.select();
                return [false, mul_msg[1]];
            }
        }
    }
    return [true, "success"]
}