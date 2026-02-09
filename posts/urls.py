from django.contrib import admin
from django.urls import path
from .import views

urlpatterns=[
     path('create_post/',views.create_post,name="create_post"),
     path('post_details/<slug>',views.post_details,name="post_details"),
     path('edit/<int:id>',views.edit_post,name="edit_post"),
     path('delete/<int:id>',views.delete_post,name="delete_post"),
     path('like/<int:id>/', views.toggle_like, name="toggle_like"),
     path('comment/<int:post_id>/', views.add_comment, name="add_comment"),
     path('comment/reply/<int:comment_id>/', views.add_reply, name="add_reply"),
     path('comment/edit/<int:comment_id>/', views.edit_comment, name="edit_comment"),
     path('comment/delete/<int:comment_id>/', views.delete_comment, name="delete_comment"),
     path('bookmark/<int:id>/',views.toggle_bookmark,name="toggle_bookmark")
]