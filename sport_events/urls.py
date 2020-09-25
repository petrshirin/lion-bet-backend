from django.urls import path, include
from .views import sports_line_view, country_line_view, \
    tournaments_line_view, matches_line_view, \
    tournaments_live_view, matches_live_view, sports_live_view, country_live_view, tournaments_with_matches_line_view, tournaments_with_matches_live_view


urlpatterns = [
    path('line/sports/', sports_line_view),
    path('line/countries/<int:sport_id>', country_line_view),
    path('line/tournaments/<int:sport_id>/<int:country_id>/<int:count>', tournaments_line_view),
    path('line/matches/<int:tournament_id>/<int:count>', matches_line_view),
    path('live/sports/', sports_live_view),
    path('live/countries/<int:sport_id>', country_live_view),
    path('live/tournaments/<int:sport_id>/<int:country_id>/<int:count>', tournaments_live_view),
    path('live/matches/<int:tournament_id>/<int:count>', matches_live_view),
    path('live/tournaments/list/<int:sport_id>', tournaments_with_matches_live_view),
    path('line/tournaments/list/<int:sport_id>', tournaments_with_matches_line_view)
]
