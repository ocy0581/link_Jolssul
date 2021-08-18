# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import numpy as np
from .model import model


lstm_model = model.LstmModel()


zeros_list = [[0,0,0]]*21

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.count = 0;
        # seq2seq model instance 생성
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print(self.scope)
        self.room_group_name = 'chat_%s' % self.room_name
        
        self.model = int
        # model upload
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



class webCamConsumers(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0
    async def connect(self):
        self.room_group_name = "TestRoom"
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # print(self.channel_name)
        await self.accept()
        self.frame_dict = dict()
        self.frame_dict[self.channel_name]=[]

    async def disconnect(self, close_code):
        
        self.frame_dict.pop(self.channel_name)

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        print('Disconnected')

    
    async def receive(self, text_data):  
        receive_dict = json.loads(text_data)

        if receive_dict['meta'] == 'end':

            result = self.predict(self.frame_dict[self.channel_name])
            await self.channel_layer.send(
                self.channel_name,
                {
                    'type' : 'send.sdp',
                    'predict_word':result,
                }   
            )

            self.frame_dict[self.channel_name].clear()
            self.count = 0;
            return

        result = self.preprocess(receive_dict)

        if (type(result) != type(None)):
            self.frame_dict[self.channel_name].append(result)

    
    async def send_sdp(self, event):
        predict_word = event['predict_word']
        # print(predict_word)
        await self.send(text_data=json.dumps({
            "message":predict_word
        }))

        
    def preprocess(self,data):

        if len(data.keys()) < 3:
            return None



        tmp_list = []
        for data_ in data['landmarks']:
            tmp = []
            for y in data_:
                tmp_j = []
                tmp_j.append(y['x'])
                tmp_j.append(y['y'])
                tmp_j.append(y['z'])
                tmp.append(tmp_j)
            tmp_list.append(tmp)


        if len(tmp_list) == 2:

            flag = 1
            if( data['handClass'][0]['label'] == 'Left'):
                flag = 0

            first = tmp_list[data['handClass'][flag]['index']].copy()
            second = tmp_list[1-data['handClass'][flag]['index']].copy()

            first.extend(second)
            tmp_list = first


        else: # 1개의 손만 인식된 경우 
            tmp_zeros = zeros_list.copy()
            tmp_list = tmp_list[0]
            if (data['handClass'][0]['label'] == 'Left'):
                tmp_list.extend(tmp_zeros)
                # print('left')
            else :                
                tmp_zeros.extend(tmp_list)
                tmp_list = tmp_zeros
                # print('right')


        print(self.count)
        self.count +=1

        print('len ',len(tmp_list))# 42가 출력되어야함

        return tmp_list

    def predict(self,data):
        datas = np.array(data)

        predict_word = lstm_model.predictWord(datas)

        print('predict',datas.shape)
        predict = str(datas.shape)
        return predict


