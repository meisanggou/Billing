/**
 * Created by msg on 12/11/16.
 */
function load_items_info(data){
    console.info(data);
    //clear_table("t_list_item");
    //var items_len = data.length;
    //var t_items = $("#t_list_item");
    //var keys = new Array("item_no", "item_name", "unit_price", "member_price");
    //var main_list = new Array();
    //var main_index = 0;
    //for(var i=0;i<items_len;i++){
    //    var tr = $("<tr id='tr_item_" + data[i].item_no + "'></tr>");
    //    if(data[i].item_no % 100 == 0) {
    //        tr.append($("<td>-</td>"));
    //        tr.append($("<td>-</td>"));
    //        tr.append($("<td>-</td>"));
    //        tr.append($("<td>-</td>"));
    //        main_list[main_index] = data[i];
    //        main_index++;
    //    }
    //    else {
    //        for (var index in keys) {
    //            tr.append(new_td(keys[index], data[i]));
    //        }
    //    }
    //    t_items.append(tr);
    //}
    //for(var j in main_list){
    //    var main_item = main_list[j];
    //    var item_id = "tr_item_" + main_item.item_no;
    //    var id_prefix = item_id.substr(0, item_id.length - 2);
    //    $("tr[id^='" + id_prefix + "']").find("td:first").text(main_item.item_name);
    //}
}

$(function(){
    $("#li_record_charge").addClass("active open");
    var item_data_url = $("#item_url").val();
    my_async_request(item_data_url, "GET", null, load_items_info);
});