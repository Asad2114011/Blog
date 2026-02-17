from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns=[
     path('add_tag/',views.add_tag,name="add_tag"),
]