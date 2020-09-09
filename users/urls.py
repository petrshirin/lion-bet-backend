
from django.contrib import admin
from django.urls import path, include
from .views import client_view, register_client_view, change_user_password_view, change_client_info_view

urlpatterns = [
    path('my/', client_view, name='my_info'),
    path('create/', register_client_view, name='new_user'),
    path('password/change/', change_user_password_view, name='my_info'),
    path('my/change/', change_client_info_view, name="change_info"),
    path('auth/', include('rest_auth.urls'), name='user_auth')
]
