/**
 * Created by msg on 5/26/16.
 */

function clear_option(select_id){
    $("#" + select_id).empty();
}

function add_option(select_id, value, text, title){
    if(title == null){
        title = text;
    }
    var option = "<option value='{value}' title='{title}'>{text}</option>";
    var option_item = option.replace("{value}", value).replace("{text}", text).replace("{title}", title);
    $("#" + select_id).append(option_item);
}

function query_option(select_id, v, query_t){
    if(query_t == null){
        query_t = "value";
    }
    if(query_t == "text"){
        var each_option = $("#" + select_id).find("option");
        var query_option = new Array();
        var fix_count = 0;
        for(var i=0;i<each_option.length;i++){
            var current_option = $(each_option[i]);
            if(current_option.text() == v){
                query_option[fix_count] = current_option;
                fix_count++;
            }
        }
    }
    else{
        var query_option = $("#" + select_id).find("[" + query_t + "='" + v + "']");
    }
    return query_option;
}

function new_td(key, obj){
    var td = $("<td></td>");
    if(key in obj){
        td.append(obj[key]);
    }
    return td;
}