from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('tmp/',views.tmp, name = "tmp"),
    # path(r'^/$',views.table), 
    path('/search/', views.search_table, name="search_table"),
]   