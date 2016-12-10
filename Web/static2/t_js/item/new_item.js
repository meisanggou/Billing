/**
 * Created by msg on 12/3/16.
 */

function load_items_info(data){
    clear_option("main_items_list");
    var items_len = data.length;
    if(items_len <= 0){
        $("#div_sub_item").hide();
    }
    for(var i=0;i<items_len;i++){
        if(data[i].item_no % 100 == 0) {
            add_option("main_items_list", data[i].item_no, data[i].item_name);
        }
    }
}

$(document).ready(function(){
	$("#li_add_item").addClass("active open");
    var item_data_url = location.href;
    $("#btn_main_item").click(function () {
        var validate_result = data_validate("div_main_item");
        if (validate_result[0] == false) {
            show_msg(validate_result[1]);
            return false;
        }
        var input_data = validate_result[1];
        if(query_option("main_items_list", input_data.item_name, "text").length > 0){
            show_msg("已经有 " + input_data.item_name + " 这个分类了，输个别的吧");
            return false;
        }
        my_async_request(item_data_url, "POST", input_data, null);
    });
    $("#btn_sub_item").click(function () {
        var validate_result = data_validate("div_sub_item");
        if (validate_result[0] == false) {
            show_msg(validate_result[1]);
            return false;
        }
        var input_data = validate_result[1];
        input_data["basic_item"] = parseInt(input_data["basic_item"]);
        input_data["unit_price"] = parseFloat(input_data["unit_price"]);
        input_data["member_price"] = parseFloat(input_data["member_price"]);
        //if(query_option("main_items_list", input_data.item_name, "text").length > 0){
        //    show_msg("已经有 " + input_data.item_name + " 这个分类了，输个别的吧");
        //    return false;
        //}
        my_async_request(item_data_url, "POST", input_data, null);
    });

    my_async_request(item_data_url, "GET", null, load_items_info);
});