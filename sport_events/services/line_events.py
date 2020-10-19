from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnList
from sport_events.betapi_wrapper import *
from sport_events.serializers import SportSerializer, CountrySerializer, \
    TournamentSerializer, MatchSerializer, SimpleMatchSerializer, MatchWithoutEventsSerializer
from django.db.models.query import Q
from typing import List, Tuple


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

    tournaments = Tournament.objects.filter(live_query_t).all()
    live_query_m = Q(request_type='line', deleted=False, ended=False)
    data = []

    low_line = page * 20
    high_line = low_line + 20

    count_matches = 0
    start_matches = 0

    total_count = Match.objects.filter(live_query_m, sport=tournaments[0].sport).count()
    for tournament in tournaments:

        len_matches = Match.objects.filter(live_query_m, tournament=tournament).count()
        start_matches += len_matches

        if start_matches < low_line:
            data += [0 for i in range(len_matches)]
            continue

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
                return data[low_line:high_line], total_count

            tmp_match = dict(match)
            tmp_match['main_events'], tmp_match['additional_events'] = split_events(match['events'])
            matches.append(tmp_match)
            count_matches += 1
        tmp_data['matches'] = matches
        data.append(tmp_data)
    return data[low_line:high_line], total_count


def split_events(events: List) -> Tuple[list, list]:
    main_events = []
    additional_events = []
    for event in events:
        if event['oc_group_name'] == '1x2' or event['oc_group_name'] == 'Тотал':
            main_events.append(event)
        else:
            additional_events.append(event)
    return main_events, additional_events


def sport_results(request: Request, sport_id: int = 0, page: int = 0) -> Tuple[ReturnList, int]:
    if sport_id:
        matches = Match.objects.filter(deleted=False, ended=True, sport_id=sport_id).all()[page*20:page*20+20]
    else:
        matches = Match.objects.filter(deleted=False, ended=True).all()[page*20:page*20+20]

    data = MatchWithoutEventsSerializer(matches, many=True).data

    return data, len(data)
