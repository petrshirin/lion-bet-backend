
from django.contrib import admin
from django.urls import path, include
from .views import create_new_request_view, opened_tech_request_view, \
    tech_support_department_view, feedback_view

urlpatterns = [
    path("request/", opened_tech_request_view, name="my_requests"),
    path("request/create/", create_new_request_view, name="new_request"),
    path("department/", tech_support_department_view, name="departments"),
    path("feedback/", feedback_view, name='feedback_view')
]
