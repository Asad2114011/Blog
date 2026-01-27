from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns=[
     path('add/',views.add_catagory,name="add_catagory")
]