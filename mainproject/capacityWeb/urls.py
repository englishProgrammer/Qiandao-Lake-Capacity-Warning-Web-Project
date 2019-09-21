from django.contrib import admin
from django.urls import path
from capacityWeb import views
urlpatterns = [
    path('index/', views.index),
    path('meifeng/', views.meifeng),

    path('getScenicHeartMapData/', views.getScenicHeartMapData)
]