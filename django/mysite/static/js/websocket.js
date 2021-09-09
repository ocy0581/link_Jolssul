

var loc = window.location;

var wsStart = 'ws://';
var host = loc.host;
if(loc.protocol == 'https:'){
    wsStart = 'wss://'
    host = loc.host.slice(0,loc.host.length-1)+1
}



var endpoint = '/ws'+loc.pathname;


var webSocket;

function checkid(){

}

function connect(){
    cover = document.querySelector('#cover');
    if(cover != undefined){
        cover.style.display = 'none'

    }
    
    webSocket = new WebSocket(
        wsStart + host + endpoint
        );
        
    // recieve 
    webSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        if (message == '사마귀') {
            document.querySelector('#chat-message-submit').onclick()
        } else {
            document.querySelector('#chat-message-input').value += (message + ' ');
        }
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        document.querySelector('#chat-log').value += (message + '\n');
        // webSocket.send(JSON.stringify({

        //     'message': message
        // }));
        //이 부분을 다른 JSON 파일로 변경하여 보낼 예정 
        messageInputDom.value = ''; 
    };
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };


    webSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

}
