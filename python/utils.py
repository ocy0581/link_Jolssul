
import torch
import os

def load_tensor(dir_names):
    '''
    tensor 가져오는 방식을 csv에서 가져온 번호에서 부터 불러오도록 설정
    output 에 nums는 현재 가져온곳의 한글값을 표현하기 위해서 
    '''
    lt_list = []
    rt_list = []
    ft_list = []
    pt_list = []
    nums = []
    for i, dir_name in enumerate(dir_names):
        path = 'output/tensor/'+dir_name[:-4]
        if not (os.path.isdir(path)):
            continue
        lt_list.append(torch.load(path+'/left_hand.pt'))
        rt_list.append(torch.load(path+'/right_hand.pt'))
        ft_list.append(torch.load(path+'/face.pt'))
        pt_list.append(torch.load(path+'/pose.pt'))
        nums.append(i)

    return lt_list, rt_list, ft_list, pt_list, nums
