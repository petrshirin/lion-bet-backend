from django.urls import path, include
from .views import create_input_request_view, create_output_request_view, \
    get_output_request_view, get_input_request_view

urlpatterns = [
    path('input/create', create_input_request_view),
    path('output/create', create_output_request_view),
    path('output/', get_output_request_view),
    path('input/', get_input_request_view),
    ]
