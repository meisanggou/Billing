/**
 * Created by msg on 12/11/16.
 */

$(document).ready(function(){
    var menu_sign = location.pathname.split("/");
    $("#li_" + menu_sign[1]).addClass("active open");
});