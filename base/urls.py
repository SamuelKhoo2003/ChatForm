from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.loginpage, name="login"), 
    path('logout/', views.logoutuser, name="logout"), 
    path('register/', views.registeruser, name="register"), 

    path('', views.home, name="home"), 
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userprofile, name="user-profile"), 

    path('create-room/', views.createroom, name="create-room"),
    path('update-room/<str:pk>/', views.updateroom, name="update-room"), 
    path('delete-room/<str:pk>/', views.deleteroom, name="delete-room"), 
    path('delete-message/<str:pk>/', views.deletemessage, name="delete-message"), 
    # path('edit-message/<str:pk>/', views.editmessage, name="edit-message"), 

    path('update-user/', views.updateruser, name="update-user"), 
]

#pk is for the primary key which is basically like an ID