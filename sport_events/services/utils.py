from django.db.models.query import Q, QuerySet
from typing import List, Tuple
from sport_events.models import Match


def calculate_tournament_with_matches_len(tournaments: QuerySet) -> int:
    count = 0
    live_query_m = Q(request_type='live', deleted=False, ended=False)
    for tournament in tournaments:

        print(Match.objects.filter(live_query_m, tournament=tournament).count())
        if Match.objects.filter(live_query_m, tournament=tournament).count():
            count += 1
    return count


def split_events(events: List) -> Tuple[list, list]:
    main_events = []
    additional_events = []
    for event in events:
        if event['oc_group_name'] == '1x2' or event['oc_group_name'] == 'Тотал':
            main_events.append(event)
        else:
            additional_events.append(event)
    return main_events, additional_events

