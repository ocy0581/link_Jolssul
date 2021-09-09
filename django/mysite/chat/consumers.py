# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import numpy as np
from .model.model import  LstmModel
from django.template.loader import render_to_string

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
            print(len(self.frame_dict[self.channel_name]))
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
            
        
        elif receive_dict['meta'] == 'error':
            self.frame_dict[self.channel_name].clear()
            self.count = 0
            return

        result = self.preprocess(receive_dict)

        if (type(result) != type(None)):
            self.frame_dict[self.channel_name].append(result)
        return 'hi'

    
    async def send_sdp(self, event):
        predict_word = event['predict_word']
        # print(predict_word)
        await self.send(text_data=json.dumps({
            "message":predict_word
        }))

        
    def preprocess(self,data):

        if len(data.keys()) < 2:
            # 3보다 작은 경우 = left,right, pose중 1개도 안잡힌경우
            return None

        keys = data.keys()
        flag = 2
        left_list = []
        if 'left' in keys:
            flag -= 1
            
            for x in data['left']:
                chunk = []
                chunk.append(x['x'])
                chunk.append(x['y'])
                chunk.append(x['z'])
                left_list.append(chunk)
            left_list = np.array(left_list)
        else :
            left_list = np.array(zeros_list)
        

        right_list = []
        if 'right' in keys:
            flag -= 1
            
            for x in data['right']:
                chunk = []
                chunk.append(x['x'])
                chunk.append(x['y'])
                chunk.append(x['z'])
                right_list.append(chunk)
            right_list = np.array(right_list)
        else :
            right_list = np.array(zeros_list)
        if flag == 2 :
            return  None
            # flag 가 2인경우 right,right가 1개도 안잡힌경우

        pose_list = []
        if 'pose' in keys:
            for x in data['pose']:
                chunk = []
                chunk.append(x['x'])
                chunk.append(x['y'])
                chunk.append(x['z'])
                pose_list.append(chunk)
            pose_list = np.array(pose_list)

        tmp_list = np.concatenate((left_list,right_list),axis=0)
        print(tmp_list.shape)
        # print(self.count)
        # self.count +=1

        # print('len ',len(tmp_list))# 42가 출력되어야함

        return tmp_list

    def predict(self,data):
        datas = np.array(data)

        predict_word = lstm_model.predictWord(datas)

        print('predict',datas.shape)
        predict = str(datas.shape)
        return predict_word



        
        # elif len(tmp_list) == 1: 
        #     print(data['handClass'][0]['label'])
        #     tmp_np = np.array(tmp_list[0])
            
        #     tmp_zeros = zeros_list
            
        #     if (data['handClass'][0]['label'] == 'Left'):
        #         tmp_list = np.concatenate((tmp_np,tmp_zeros),axis=0)



        # tmp_list = []
        # for data_ in data['landmarks']:
        #     tmp = []
        #     for y in data_:
        #         tmp_j = []
        #         tmp_j.append(y['x'])
        #         tmp_j.append(y['y'])
        #         tmp_j.append(y['z'])
        #         tmp.append(tmp_j)
        #     tmp_list.append(tmp)


        # if len(tmp_list) == 2:

        #     flag = 1
        #     if( data['handClass'][0]['label'] == 'Right'):
        #         flag = 0

        #     first = tmp_list[data['handClass'][flag]['index']].copy()
        #     second = tmp_list[1-data['handClass'][flag]['index']].copy()

        #     first.extend(second)
        #     tmp_list = first


        # elif len(tmp_list) == 1: # 1개의 손만 인식된 경우 
        #     tmp_zeros = zeros_list.copy()
        #     tmp_list = tmp_list[0]
        #     if (data['handClass'][0]['label'] == 'Right'):
        #         tmp_list.extend(tmp_zeros)
        #         # print('left')
        #     else :                
        #         tmp_zeros.extend(tmp_list)
        #         tmp_list = tmp_zeros
        #         # print('right')
