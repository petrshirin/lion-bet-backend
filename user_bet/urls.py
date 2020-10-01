from django.urls import path, include
from .views import make_bet_view, find_bet_for_ticket_view, get_all_user_bet_view

urlpatterns = [
    path('make/<str:bet_type>', make_bet_view),
    path('userbets/', get_all_user_bet_view),
    path('ticket/<str:ticket>', find_bet_for_ticket_view),
]
