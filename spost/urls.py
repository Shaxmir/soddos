from django.urls import path
from .views import *

urlpatterns = [
    path('post/', post, name="post"),
    path('post/<int:id>/', post, name="post_detali"),
    path('post/create_post/', create_post, name="create_post"),
    path('post/<int:id>/del_post/', del_post, name='del_post'),
    path('post/<int:id>/edit_post/', edit_post, name='edit_post'),
]