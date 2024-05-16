
from django.contrib import admin
from django.urls import path

from store.views import index, about, contact,wishlist
urlpatterns = [
   path('', index, name='index'),
   path('about', about, name='about'),
   path('contact', contact, name='contact'),
   path('wishlist', wishlist, name='wishlist'),
   
]
