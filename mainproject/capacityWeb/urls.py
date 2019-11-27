from django.contrib import admin
from django.urls import path
from capacityWeb import views

app_name = '[capacityWeb]'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('meifeng/', views.meifeng, name='meifeng'),
    path('huangshanjian/', views.huangshanjian, name='huangshanjian'),
    path('tianchi/', views.tianchi, name='tianchi'),
    path('yueguang/', views.yueguang, name='yueguang'),
    path('longshan/', views.longshan, name='longsha'),
    path('yule/', views.yule, name='yule'),
    path('guihua/', views.guihua, name='guihua'),
    path('mishan/', views.mishan, name='mishan'),
    path('updatetodayTouristNums/', views.updatetodayTouristNums),
    path('updatetodayTouristNums2/', views.updatetodayTouristNums2),
    path('getScenicHeartMapData/', views.getScenicHeartMapData),
    path('admin/', views.admin, name='admin'),
    path('getAdminData/', views.getAdminData),
    path('deleteAdminData/', views.deleteAdminData),
    path('addAdminData/', views.addAdminData)
]