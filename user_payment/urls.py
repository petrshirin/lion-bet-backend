from django.urls import path, include
from .views import input_request_view, output_request_view

urlpatterns = [
    path('input/', input_request_view),
    path('output/', output_request_view),
    ]
