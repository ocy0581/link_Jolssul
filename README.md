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

### redis 설치(window)

https://github.com/tporadowski/redis/releases

Redis-x64-5.0.10.msi 실행

### django_channels pip 설치

``` pip install django ```

``` pip install channels ```

``` pip install channels_redis ```


### django 실행

터미널에서 ~~~~\django\mysite> 까지 이동
> ex: ``` C:\Users\user\Documents\Github\link_Jolssul\django\mysite> ```

이후 ``` python manage.py runserver ``` 입력

> ex: ``` C:\Users\user\Documents\Github\link_Jolssul\django\mysite > python manage.py runserver ```

### 실시간 채팅 사용법

1. http://127.0.0.1:8000/chat/ 에 접속

2. textarea에 아무 문자열(ex: tmp, lobby) 입력
   >(lobby입력했다 가정) http://127.0.0.1:8000/chat/lobby/ 로 이동

3. 접속된 웹 페이지 안에는 textarea가 2개 있고 큰 곳에는 채팅이 보이고 작은곳에 채팅을 입력할 수 있다.

4. 다른 브라우저(다른 탭)에서 똑같이  http://127.0.0.1:8000/chat/lobby/ 에 접속하거나  http://127.0.0.1:8000/chat/ 접속해서 textarea에 직전에 입력한 문자열 입력(예시로 lobby)

5. 들어온 곳에서 작은 textarea에 문자입력후 send 클릭 혹은 엔터 입력시 전송되며 접속중인 브라우저의 큰 textarea에 글자가 반영된다.