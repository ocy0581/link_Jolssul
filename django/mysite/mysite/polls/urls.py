from django.urls import path

from . import views

app_name= 'polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('tmp/',views.tmp, name = "tmp/"),
    path('tmp',views.tmp, name = "tmp"),
    ]   

#url을 분석해서 해당 함수를 호출하는 곳
