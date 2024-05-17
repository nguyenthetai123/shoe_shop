from auths.views import register,activate
from .views import LoginView
from django.contrib import admin
from django.urls import path

urlpatterns = [
   path('register', register, name='register'),
   path('login', LoginView.as_view(), name="login"),
   path('activate/<uidb64>/<token>', activate, name='activate'),
   
]
