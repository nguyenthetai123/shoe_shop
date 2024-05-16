from auths.views import register
from django.contrib import admin
from django.urls import path

urlpatterns = [
   path('register', register, name='register')
]
