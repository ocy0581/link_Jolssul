## 데이터셋

- kinetics-skeleton
- ntu-xsub
- ntu-xview

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
  
---

- TODO
  - train 방법
  - dataset 형태
  - 데이터 전처리 과정
  - 논문 확인
  - argument 사용법 및 디버그 사용법
    
    
