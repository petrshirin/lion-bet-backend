from django.db.models.query import Q, QuerySet
from typing import List, Tuple
from sport_events.models import Match, Tournament
from sport_events.serializers import SimpleMatchSerializer, TournamentSerializer


EVENTS_TO_INT = {
    "П1": 1,
    "Х": 2,  # ru
    "X": 2,  # eng
    "П2": 3,
    "ТМ": 4,
    "ТБ": 5,
    "1Х": 6,  # ru
    "1X": 6,  # eng
    "12": 7,
    "2Х": 8,  # ru
    "2X": 8,  # eng
    "ИТМ1": 9,
    "ИТБ1": 10,
    "ИТМ2": 11,
    "ИТБ2": 12,
    "Нет": 13,
    "Да": 14,
    "Ф": 15,
    "*": 100,
}


def delete_void_tournaments(tournaments: QuerySet, request_type: str = 'line') -> List:
    tournaments_with_matches = []
    live_query_m = Q(request_type=request_type, deleted=False, ended=False)
    for tournament in tournaments:

        if Match.objects.filter(live_query_m, tournament=tournament).count():
            tournaments_with_matches.append(tournament)
    return tournaments_with_matches


def split_events(events: List) -> Tuple[list, list]:
    main_events = []
    additional_events = []
    for event in events:
        if event['oc_group_name'] == '1x2' or event['oc_group_name'] == 'Тотал':
            main_events.append(event)
        else:
            additional_events.append(event)
    main_events.sort(key=sort_event)
    additional_events.sort(key=sort_event)
    return main_events, additional_events


def sort_event(event: dict) -> int:
    return EVENTS_TO_INT.get(event['short_name'].split(' ')[0], '*')


def generate_page_of_tournaments(page: int, query_t: Q, query_m: Q, request_type: str = 'line') -> Tuple[List, int]:
    tournaments = Tournament.objects.filter(query_t).all()
    low_line = page * 5
    data = []

    count_tournaments = 0

    tournaments = delete_void_tournaments(tournaments, request_type=request_type)

    for tournament in tournaments[low_line:]:
        if count_tournaments >= 5:
            break

        matches = Match.objects.filter(query_m, tournament=tournament).all()

        if not matches:
            continue
        matches_ser = SimpleMatchSerializer(matches, many=True)
        tournament_ser = TournamentSerializer(tournament)
        tmp_data = dict(tournament_ser.data)
        matches = []
        for match in matches_ser.data:
            tmp_match = dict(match)
            tmp_match['main_events'], tmp_match['additional_events'] = split_events(match['events'])
            matches.append(tmp_match)
        tmp_data['matches'] = matches
        data.append(tmp_data)
        count_tournaments += 1
    return data, len(tournaments)


