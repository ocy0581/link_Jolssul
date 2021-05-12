import torch
import random
import math

class DataAugmentation(object):
    '''
    독립적으로 진행 
    손1개로 일단 제작중

------------------------------------------
    eps의 확률로 좌우 중에 scale만큼 이동
    eps의 확률로 상하 중에 scale만큼 이동
    
 -------------------------------------------   구현완료

    구현중
    1/4의 확률로 x축 축소 
    1/4의 확률로 y축 축소

    '''
    def __init__(self, sample_data,max_scale=0.05,eps = 0.5,device = 'cpu' ):
        self.eps = eps
        if(eps > 1 ):
            self.eps = 1


        self.data_shape = sample_data.shape
        self.x = torch.FloatTensor([1,0,0]*self.data_shape[0]).repeat(self.data_shape[0]*self.data_shape[1]
        ).reshape(self.data_shape).to(device)
        self.y = torch.FloatTensor([0,1,0]*self.data_shape[0]).repeat(self.data_shape[0]*self.data_shape[1]
        ).reshape(self.data_shape).to(device)
        self.z = torch.FloatTensor([0,0,1]*self.data_shape[0]).repeat(self.data_shape[0]*self.data_shape[1]
        ).reshape(self.data_shape).to(device)

        self.scale = max_scale

    def __call__(self, data ):
        
        # x축 증식
        if(random.random() < self.eps):
            data += self.x * (random.random()*self.scale*2 - self.scale)
            # print('x증식 =======================\n{}\n============'.format(data[0,0]))
        # y축 증식
        if(random.random() < self.eps):
            data += self.y * (random.random()*self.scale*2 - self.scale)
            # print('y증식=======================\n{}\n============'.format(data[0,0]))

        # x축 회전 및 중앙정렬
        if(random.random() < self.eps):
            rand = random.random()*self.scale*2+(1-self.scale)
            data = data.mul(self.x*rand+self.y+self.z) + self.x*(1-rand)/2
            # print(rand)
            # print('x,회전=======================\n{}\n============'.format( data[0,0]))
        
        # y축 회전 및 중앙정렬
        if(random.random() < self.eps):
            rand = random.random()*self.scale*2+(1-self.scale)
            data = data.mul(self.x+self.y*rand+self.z) + self.y*(1-rand)/2
            # print(rand)
            # print('y,회전=======================\n{}\n============'.format(data[0,0]))
        # tmp = x + data + z
        # print(tmp[0][0])
        return data

    
if __name__ == '__main__':
    data_shape = (192,32,63)
    max_scale = 0.1
    a = torch.FloatTensor([0.7,0.7,0.7]*21).repeat(data_shape[0]*data_shape[1]).reshape(data_shape)

    model = DataAugmentation(a,0.01,1)
    print(a[0][0])
    t = []
    for x in range(1000):
        t.append(model(a)[0][0][:3])
        # print(t[-1])
    
    avg_x = sum([x[0] for x in t])/len(t)
    avg_y = sum([x[1] for x in t])/len(t)
    print(avg_x,avg_y)