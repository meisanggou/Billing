/**
 * Created by msg on 12/11/16.
 */
function load_items_info(data){
    console.info(data);
    //clear_table("t_list_item");
    var items_len = data.length;
    for(var i=0;i<items_len;i++) {
        var one_item = data[i];
        var price_s = one_item. unit_price + "," + one_item.member_price;
        if (one_item.item_no % 100 == 0) {
            add_option("main_item", one_item.item_no, one_item.item_name, price_s);
        }
        else{
            add_option("sub_item", one_item.item_no, one_item.item_name, price_s);
        }
    }
    $("#main_item").change(function(){
        var basic_no = parseInt($(this).val());
        $("#sub_item option").each(function(){
            var item_no = parseInt($(this).val());
            if(item_no>basic_no && item_no<basic_no+100){
                $(this).show();
            }else{
                $(this).hide();
            }
        });
        var first_option = $("#sub_item option:visible").eq(0);
        if(first_option.length<=0){
            console.info("no sub item");
            $("#sub_item").find("option:eq(0)").show();
        }
        first_option.attr("selected", true);
        $("#sub_item").find("option:visible").eq(0).attr("selected", true);
    });
    $("#main_item").change();
}

$(function(){
    $("#li_record_charge").addClass("active open");
    var item_data_url = $("#item_url").val();
    my_async_request(item_data_url, "GET", null, load_items_info);
});

//  注册时间响应
$(function(){
    $("select[name='is_member']").change(function(){
        var is_member = $(this).val();
        if(is_member == 1){
            $("#div_is_member").show();
            $("#div_not_member").hide();
        }
        else{
            $("#div_is_member").hide();
            $("#div_not_member").show();
        }
    });
    $("select[name='is_member']").change();
});