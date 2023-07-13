from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name="home"), 
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/', views.createroom, name="create-room")
]

#pk is for the primary key which is basically like an ID