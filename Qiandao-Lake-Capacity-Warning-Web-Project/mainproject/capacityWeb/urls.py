from django.contrib import admin
from django.urls import path
from capacityWeb import views

app_name = '[capacityWeb]'
urlpatterns = [
    # 主页
    path('index/', views.index, name='index'),
    # 各景区详细信息
    path('meifeng/', views.meifeng, name='meifeng'),
    path('huangshanjian/', views.huangshanjian, name='huangshanjian'),
    path('tianchi/', views.tianchi, name='tianchi'),
    path('yueguang/', views.yueguang, name='yueguang'),
    path('longshan/', views.longshan, name='longsha'),
    path('yule/', views.yule, name='yule'),
    path('guihua/', views.guihua, name='guihua'),
    path('mishan/', views.mishan, name='mishan'),
    path('updatetodayTouristNums/', views.updatetodayTouristNums),
    path('getScenicHeartMapData/', views.getScenicHeartMapData),

]