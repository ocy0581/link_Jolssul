# KOREATECH link 15th 졸업설계 repository

---

## Python mediapipe env setting


### 가상환경 생성
```conda create -n mp_env python=3.8```

### 가상환경 활성화
```conda activate mp_env```

### mediapipe 설치
```pip install mediapipe```

### pytorch 설치
```conda install pytorch torchvision torchaudio -c pytorch```

### jupyterlab 설치
```conda install -c conda-forge jupyterlab```

### jupyterlab 실행
```jupyter-lab```

---

## django setting

redis

https://github.com/tporadowski/redis/releases

Redis-x64-5.0.10.msi

위에것 설치 이후에 사용가능

pip 목록

pip install django
pip install channels
pip install channels_redis


사용법

터미널에서 ~~~~\django\mysite> 까지 이동 이후

\django\mysite> python manage.py runserver 

입력시 127.0.0.1:8000/에 접속가능

여기서 인터넷 주소창에 
http://127.0.0.1:8000/chat/

입력 하면 화면에 text 넣을수 있는 창이 있음

그 textarea에 아무 문자열(ex: tmp, lobby) 입력하면 (tmp입력했다 가정)
http://127.0.0.1:8000/chat/tmp/
로 접속됨 이 안에는 textarea가 2개 있고 큰 곳에는 채팅이 보이고 작은곳에 채팅을 입력할 수 있음

다른 브라우저(다른 탭)에서 똑같이 http://127.0.0.1:8000/chat/tmp/ 에 들어오거나  
http://127.0.0.1:8000/chat/ 들어와서 textarea에 위에서 입력한 문자 입력(예시로 tmp)

들어온 곳에서 작은 곳에 문자입력후 send 클릭 혹은 엔터 입력시 전송되고 브라우저 모두 큰 textarea에 글자가 반영됨


추가로 만들어야되는것

connect 될때 모델을 생성한다면 생성되는 모델이 전부 다 다른 모델인지 확인
모델에 정보를 보낼때 다른 정보도 보낼수 있는지 확인
모델 타입이 json인지 다른 타입인지 확인
