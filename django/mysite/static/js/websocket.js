

var loc = window.location;

var wsStart = 'ws://';
var host = loc.host;
if(loc.protocol == 'https:'){
    wsStart = 'wss://'
    host = loc.host.slice(0,loc.host.length-1)+1
}



var endpoint = '/ws'+loc.pathname;


var chatSocket;

function checkid(){

}

function connect(){
    cover = document.querySelector('#cover');
    if(cover != undefined){
        cover.style.display = 'none'

    }
    
    chatSocket = new WebSocket(
        wsStart + host + endpoint
        );
        
    // recieve 
    chatSocket.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var message = data['message'];
        document.querySelector('#chat-log').value += (message + '\n');
    };

    document.querySelector('#chat-message-submit').onclick = function(e) {
        var messageInputDom = document.querySelector('#chat-message-input');
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({

            'message': message
        }));
        //이 부분을 다른 JSON 파일로 변경하여 보낼 예정 
        messageInputDom.value = ''; 
    };
    document.querySelector('#chat-message-input').focus();
    document.querySelector('#chat-message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#chat-message-submit').click();
        }
    };


    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

}
