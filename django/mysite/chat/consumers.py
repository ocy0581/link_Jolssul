# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import numpy as np
from .model.model import  LstmModel


lstm_model = LstmModel()
zeros_list = np.array([[0,0,0]]*21)

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
            self.count = 0
            return

        result = self.preprocess(receive_dict)

        if (len(result) != 0):
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

        
        elif len(tmp_list) == 1: 
            print(data['handClass'][0]['label'])
            tmp_np = np.array(tmp_list[0])
            
            tmp_zeros = zeros_list
            
            if (data['handClass'][0]['label'] == 'Left'):
                tmp_list = np.concatenate((tmp_np,tmp_zeros),axis=0)

            else :                
                tmp_list = np.concatenate((tmp_zeros,tmp_np),axis=0)

            print(tmp_list)
        return tmp_list

    def predict(self,data):
        datas = np.array(data)
        predict_word = lstm_model.predictWord(datas)
        print('input shape: ',datas.shape,' predict: ',predict_word)
        return predict_word
 