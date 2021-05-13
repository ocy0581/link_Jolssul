## 데이터셋

- kinetics-skeleton
  - data = kinetics-skeleton/train_data.npy
  - data.shape : (240436, 3, 300, 18, 2)
- ntu-xsub
  - data = NTU-RGB-D/xsub/train_data.npy
  - data.shape : ( 40091, 3, 300, 25, 2)
- ntu-xview
  - data = NTU-RGB-D/xsub/train_data.npy
  - data.shape : ( 37646, 3, 300, 25, 2)


## input data shape(net.st_gcn.Model.__init__())

- (N, C, T, V, M)
  - N: batch size
  - C: in_channel 
  - T: 인풋 시퀀스 길이
  - V: 그래프 노드의 수
  - M: 프레임의 인스턴스 수(프레임 길이 말하는 듯)
- kinetics-skeleton
  - (N, C, T, V, M) : (N, 3, 300, 18, 2)
- ntu-xsub
  - (N, C, T, V, M) : (N, 3, 300, 25, 2)
- ntu-xview
  - (N, C, T, V, M) : (N, 3, 300, 25, 2)
  

## mediapipe data shape(link_Jolssul.python.output.tentsor)

- (T, V, C)
  - T: time step(파일 마다 다름, 통상 130~169 사이 정도 )
  - V: 그래프 노드의 수
  - C: x, y, z
- KETI_SL_0000000002/left_hand.pt
  - (T, V, C) : (160, 21, 3)
- KETI_SL_0000000002/pose.pt
  - (T, V, C) : (160, 33, 3)
- KETI_SL_0000000003/left_hand.pt
  - (T, V, C) : (123, 21, 3)
- KETI_SL_0000000003/pose.pt
  - (T, V, C) : (123, 33, 3)
- 부위별 노드 개수(V#)
  - right_hand : 21
  - left_hand : 21
  - pose : 33
  - face : 468
  


## 디렉토리 및 파일 설명

- config : configuration files
  - *.yaml
    - data, label, weight 경로 설정 
    - model 클래스
    - batch_size, dropout 등 각종 하이퍼 파라미터 설정
    - train 실행 기본 포맷
      - ```python main.py recognition -c config/st_gcn/<dataset>/train.yaml [--work_dir <work folder>]```
    - test 실행 기본 포맷
      - ```python main.py recognition -c config/st_gcn/<dataset>/test.yaml --weights <path to model weights>```
    - test 예시(weight path는 yaml에 지정해줘서 안 적은 듯)
      - ```python main.py recognition -c config/st_gcn/kinetics-skeleton/test.yaml```
      - ```python main.py recognition -c config/st_gcn/ntu-xview/test.yaml```
      - ```python main.py recognition -c config/st_gcn/ntu-xsub/test.yaml```
  
- data : dataset
  - 용량이 50GB가 넘기에 gitignore 되어 있음
  - *_train
    - Kinetics-skeleton(원본 데이터)
      - download link : [Kinetics-skeleton](https://drive.google.com/drive/folders/1SPQ6FmFsjGg3f59uCWfdUWI-5HJM_YhZ)
    - NTU RGB+D(원본 데이터)
      - download link : [NTU RGB+D](http://rose1.ntu.edu.sg/datasets/actionrecognition.asp)
  - [train | val]_[data.npy | label.pkl]
    - 전처리된 데이터
    - download link : [GoogleDrive](https://drive.google.com/file/d/103NOL9YYZSW1hLoWmYnv5Fs8mK-Ij7qb/view)
    - 또는 다음 코드 실행으로 생성 가능
      - ```python tools/kinetics_gendata.py --data_path <path to kinetics-skeleton>```
      - ```python tools/ntu_gendata.py --data_path <path to nturgbd+d_skeletons>```
    
- feeder : ?
- models/
  - pose/ : ?
  - *.pt : 가중치 파일  
    - ```bash tools/get_models.sh```  
      실행으로 사전 훈련 모델 가중치 다운로드 가능
- net : 실질적인 네트워크 모델
- processor
  - main.py 실행 때 사용되는 argument 설정 등
- resource
  - readme.md 작성 용 사진, gif
  - 참고자료
- tools
  - get_models.sh : 사전 훈련 가중치 파일 다운로드 쉘 명령어 
  - *_gendata.py : 데이터 전처리 작업 util 파일
- torchlight : torchlight 설치 파일
  - ```cd torchlight; python setup.py install;```
- work_dir
  - 다음 명령(train 실행)을 실행할 때 사용되는 디렉토리
  - ```python main.py recognition -c config/st_gcn/<dataset>/train.yaml [--work_dir <work folder>]```
  - work_dir 안에서 파일이나 디렉토리를 만들어 줄 필요 없음
  - 출력물이 나오는 디렉토리라고 생각하면 됨
  - work_dir 지정은 위 명령줄에서 인수로 추가해주거나 train.yaml의 line 1에서 지정 가능
  
---

- TODO
  - train 방법
  - dataset 형태
  - 데이터 전처리 과정
  - 논문 확인
  - argument 사용법 및 디버그 사용법
    
    
