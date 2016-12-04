/**
 * Created by msg on 12/3/16.
 */

function load_items_info(data){
    clear_option("main_items_list");
    var items_len = data.length;
    for(var i=0;i<items_len;i++){
        add_option("main_items_list", data[i].item_no, data[i].item_name);
    }
    query_option("main_items_list", "项目", "text");
}

$(document).ready(function(){
	$("#li_add_item").addClass("active open");

    var item_data_url = location.href;
    my_async_request(item_data_url, "GET", null, load_items_info);
});