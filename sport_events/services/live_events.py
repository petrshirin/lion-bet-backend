from rest_framework.utils.serializer_helpers import ReturnList
from sport_events.betapi_wrapper import *
from sport_events.serializers import TournamentSerializer, MatchSerializer, SportSerializer, CountrySerializer, SimpleMatchSerializer
from django.db.models.query import Q
from .line_events import split_events
from typing import List, Tuple


def get_live_sports() -> ReturnList:
    sports = Sport.objects.filter(deleted=False, request_type='live').all()
    return SportSerializer(sports, many=True).data


def get_live_countries(sport_id: int = None) -> ReturnList:
    if sport_id:
        countries = Country.objects.filter(sport__api_id=sport_id, deleted=False, request_type='live').all()
    else:
        countries = Country.objects.filter(deleted=False, request_type='live').all()
    return CountrySerializer(countries, many=True).data


def get_live_tournaments(sport_id: int = None, country_id: int = None, count: int = None) -> ReturnList:
    live_query = Q(request_type='live', deleted=False)
    if sport_id and country_id:
        all_query = Q(sport__api_id=sport_id, country__api_id=country_id)
        tournaments = Tournament.objects.filter(all_query, live_query).all()
    elif sport_id:
        sport_query = Q(sport__api_id=sport_id)
        tournaments = Tournament.objects.filter(sport_query, live_query).all()
    elif country_id:
        country_query = Q(country__api_id=country_id)
        tournaments = Tournament.objects.filter(country_query, live_query).all()
    else:
        tournaments = Tournament.objects.filter(live_query).all()
    if count:
        tournaments = tournaments[:count]
    return TournamentSerializer(tournaments, many=True).data


def get_live_matches(tournament_id: int = None, count: int = None) -> ReturnList:
    live_query = Q(request_type='live', deleted=False, ended=False)
    if tournament_id:
        tournament_query = Q(tournament__api_id=tournament_id)
        matches = Match.objects.filter(tournament_query, live_query).all()
    else:
        matches = Match.objects.filter(live_query).all()

    if count:
        matches = matches[:count]

    return MatchSerializer(matches, many=True).data


def get_list_of_tournaments_with_matches_live(sport_id: int = 0, page: int = 0) -> Tuple[List, int]:
    if sport_id:
        live_query_t = Q(request_type='live', deleted=False, sport__api_id=sport_id)
    else:
        live_query_t = Q(request_type='live', deleted=False)

    tournaments = Tournament.objects.filter(live_query_t).all()
    live_query_m = Q(request_type='live', deleted=False, ended=False)

    low_line = page * 20
    high_line = low_line + 20
    data = []

    count_matches = 0
    total_count = Match.objects.filter(live_query_m, sport=tournaments[0].sport).count()
    for tournament in tournaments:

        matches = Match.objects.filter(live_query_m, tournament=tournament).all()

        if not matches:
            continue
        matches_ser = SimpleMatchSerializer(matches, many=True)
        tournament_ser = TournamentSerializer(tournament)
        tmp_data = dict(tournament_ser.data)
        matches = []
        for match in matches_ser.data:
            if count_matches >= high_line:
                tmp_data['matches'] = matches
                data.append(tmp_data)
                return data, total_count

            tmp_match = dict(match)
            tmp_match['main_events'], tmp_match['additional_events'] = split_events(match['events'])
            matches.append(tmp_match)
            count_matches += 1
        tmp_data['matches'] = matches
        data.append(tmp_data)
    return data[low_line:high_line], total_count
