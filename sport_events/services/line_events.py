from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnList
from sport_events.betapi_wrapper import *
from sport_events.serializers import SportSerializer, CountrySerializer, \
    TournamentSerializer, MatchSerializer, SimpleMatchSerializer, MatchWithoutEventsSerializer
from django.db.models.query import Q
from typing import List, Tuple
from .utils import split_events, delete_void_tournaments, generate_page_of_tournaments



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


def get_list_of_tournaments_with_matches_line(sport_id: int = 0, page: int = 0) -> Tuple[List, int]:
    if sport_id:
        live_query_t = Q(request_type='line', deleted=False, sport__api_id=sport_id)
    else:
        live_query_t = Q(request_type='line', deleted=False)

    live_query_m = Q(request_type='line', deleted=False, ended=False)

    return generate_page_of_tournaments(page, live_query_t, live_query_m)


def sport_results(sport_id: int = 0, page: int = 0) -> Tuple[List, int]:
    if sport_id:
        query_t = Q(deleted=False, sport__api_id=sport_id)
    else:
        query_t = Q(deleted=False)

    query_m = Q(deleted=False, ended=True)

    return generate_page_of_tournaments(page, query_t, query_m)
