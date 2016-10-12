/**
 * Created by msg on 10/12/16.
 */
var ws_service = location.host;
    var ws = new WebSocket('ws://' + ws_service + '/chat/msg/');
    ws.onmessage = function(event) {
        var table = document.getElementById('chat_message');
        var msg = JSON.parse(event.data);
        var insert_row = table.insertRow();
        insert_row.insertCell().innerHTML = msg["sender"];
        insert_row.insertCell().innerHTML = msg["msg"];
    };
    ws.onopen = function(event) {
        var current_user_name = $("#current_user_name").val();
        var login_msg = JSON.stringify({"msg_type": "login", "data": current_user_name});
        ws.send(login_msg);
    };
    function send() {
        var msg_info = JSON.stringify({"msg_type": "msg", "data": document.getElementById('chat').value});
        ws.send(msg_info);
        document.getElementById('chat').value = '';
}