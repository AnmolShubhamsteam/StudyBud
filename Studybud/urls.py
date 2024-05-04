"""
URL configuration for Studybud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home.views import *
urlpatterns = [
    path("login/",login_page,name="login"),
    path("logout/",log_out,name="logout"),
    path("register/",registerUser,name="register"),
    path("",home,name="home"),
    path("room/<str:pk>/",room,name="room"),
    path("admin/",admin.site.urls),
    path("create-room/",createRoom,name="createroom"),
    path("update-room/<str:pk>",updateRoom,name="updateroom"),
    path("delete-room/<str:pk>",deleteRoom,name="deleteroom"),
    path("delete-message/<str:pk>",deleteMessage,name="deletemessage"),
]
