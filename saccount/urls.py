from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('locked_out.html/', logout_view, name='logout'),
    path('profile/', profile, name="profile"),
    path('profile/edit_profile/', edit_profile, name="edit_profile")
]

