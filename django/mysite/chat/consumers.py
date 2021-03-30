# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # seq2seq model instance 생성
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        

    async def disconnect(self, close_code):
        # Leave room group
        # seq2seq model 제거 (del model)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):  
        # 수신받은 json data의 전처리이후 모델에 입력하여 text출력
        # 속도에 따라서 받을 때 마다가 아닌 일정 간격을 모델에 입력해야 할 수도 있음
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("receive {0}".format(message) )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # text를 다시 json파일로 변경 후 송신
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

