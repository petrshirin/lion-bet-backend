"""lion_bet_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from user_bet.views import process_bet_view

urlpatterns = [
    path('default/admin/', admin.site.urls),
    path('user/', include('users.urls'), name='users'),
    path('support/', include('techsupport.urls'), name='techsupport'),
    path('sport_events/', include('sport_events.urls'), name='sport_events'),
    path('payments/', include('user_payment.urls'), name="payments"),
    path('bet/', include('user_bet.urls'), name='user_bet'),
    path('api/bet/result', process_bet_view),
    path('admin_tools/', include('admin_tools.urls')),
    path('ajax_select/', include('ajax_select.urls')),
]
