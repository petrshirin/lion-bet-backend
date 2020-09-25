from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnList
from sport_events.betapi_wrapper import *
from sport_events.serializers import SportSerializer, CountrySerializer, TournamentSerializer, MatchSerializer, SimpleMatchSerializer
from django.db.models.query import Q
from typing import List


def get_line_sports() -> ReturnList:
    sports = Sport.objects.filter(deleted=False, request_type='line').all()
    return SportSerializer(sports, many=True).data


def get_line_countries(sport_id: int = None) -> ReturnList:
    if sport_id:
        countries = Country.objects.filter(sport__api_id=sport_id, deleted=False, request_type='line').all()
    else:
        countries = Country.objects.filter(deleted=False, request_type='line').all()
    return CountrySerializer(countries, many=True).data


def get_line_tournaments(sport_id: int = None, country_id: int = None, count: int = None) -> ReturnList:
    line_query = Q(request_type='line', deleted=False)
    if sport_id and country_id:
        all_query = Q(sport__api_id=sport_id, country__api_id=country_id)
        tournaments = Tournament.objects.filter(all_query, line_query).all()
    elif sport_id:
        sport_query = Q(sport__api_id=sport_id)
        tournaments = Tournament.objects.filter(sport_query, line_query).all()
    elif country_id:
        country_query = Q(country__api_id=country_id)
        tournaments = Tournament.objects.filter(country_query, line_query).all()
    else:
        tournaments = Tournament.objects.filter(line_query).all()
    if count:
        tournaments = tournaments[:count]
    return TournamentSerializer(tournaments, many=True).data


def get_line_matches(tournament_id: int = None, count: int = None) -> ReturnList:
    line_query = Q(request_type='line', deleted=False, ended=False)
    if tournament_id:
        tournaments_query = Q(tournament__api_id=tournament_id)
        matches = Match.objects.filter(tournaments_query, line_query).all()
    else:
        matches = Match.objects.filter(line_query).all()

    if count:
        matches = matches[:count]

    return MatchSerializer(matches, many=True).data


def get_list_of_tournaments_with_matches_line(sport_id: int = 0) -> List:
    if sport_id:
        live_query_t = Q(request_type='line', deleted=False, sport__api_id=sport_id)
    else:
        live_query_t = Q(request_type='line', deleted=False)

    tournaments = Tournament.objects.filter(live_query_t).all()
    live_query_m = Q(request_type='line', deleted=False, ended=False)
    data = []
    for tournament in tournaments:
        matches = Match.objects.filter(live_query_m, tournament=tournament).all()
        matches_ser = SimpleMatchSerializer(matches, many=True)
        tournament_ser = TournamentSerializer(tournament)
        tmp_data = dict(tournament_ser.data)
        tmp_data['matches'] = matches_ser.data
        data.append(tmp_data)
    return data


