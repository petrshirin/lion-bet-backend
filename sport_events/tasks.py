from celery.task import periodic_task
from celery.schedules import crontab
from .betapi_wrapper import SportWrapper, CountryWrapper, TournamentWrapper, MatchWrapper, CurrentMatchWrapper, Match
from celery import Celery
from lion_bet_backend.celery import app
import logging
from user_bet.models import UserBet
from .models import MatchAdminResult
from django.utils.timezone import now


LOG = logging.getLogger(__name__)


@app.task
def update_countries_line():
    country_api = CountryWrapper()
    country_api.save_items_to_db()
    LOG.info('update line countries completed')


@app.task
def update_tournaments_line():
    tournament_api = TournamentWrapper()
    tournament_api.save_items_to_db()
    LOG.info('update line tournaments completed')


@app.task
def update_matches_line():
    matches_api = MatchWrapper()
    matches_api.save_items_to_db()
    LOG.info('update line matches completed')


@app.task
def update_countries_live():
    country_api = CountryWrapper('live')
    country_api.save_items_to_db()
    LOG.info('update live countries completed')


@app.task
def update_tournaments_live():
    tournament_api = TournamentWrapper('live')
    tournament_api.save_items_to_db()
    LOG.info('update live tournaments completed')


@app.task
def update_matches_live():
    matches_api = MatchWrapper('live')
    matches_api.save_items_to_db()
    LOG.info('update live matches completed')


@app.task
def close_matches():
    for match in Match.objects.filter(deleted=False, ended=False, admin_created=False, game_start__lte=now()).all():
        current_match_api = CurrentMatchWrapper(request_type=match.request_type, game_id=match.game_num, uniq=match.uniq)
        current_match_api.close_current_match(match)


@app.task
def close_results_for_admin_matches():
    matches = Match.objects.filter(deleted=False, ended=False, admin_created=True, game_start__lte=now()).all()
    print(matches)
    for match in matches:
        result = MatchAdminResult.objects.filter(match=match, date_closed__lte=now()).first()
        if not result:
            continue
        match.ended = True
        match.score_full = result.total_score
        match.save()
        for event in match.events.all():
            user_bets = UserBet.objects.filter(events__exact=event).all()
            print(user_bets)
            for user_bet in user_bets:
                if len(user_bet.events.all()) > 1:
                    pass
                else:
                    user_event = user_bet.events.first()
                    if user_event.oc_group_name == '1х2' or user_event.oc_group_name == '1x2':
                        if result.winner == 'П1':
                            command_winner = match.opp_1_name
                        elif result.winner == 'П2':
                            command_winner = match.opp_1_name
                        else:
                            command_winner = 'X'
                        if user_event.oc_name == command_winner:
                            user_bet.user.customeraccount.current_balance += user_bet.user_win
                            user_bet.is_went = True
                        else:
                            user_bet.is_went = False
                            user_bet.user.customeraccount.current_balance -= user_bet.user_bet
                    elif user_event.oc_group_name.lower() == 'тотал':
                        user_event = user_bet.events.first()
                        if result.total in user_event.oc_name:
                            user_bet.user.customeraccount.current_balance += user_bet.user_win
                            user_bet.is_went = True
                        else:
                            user_bet.is_went = False
                            user_bet.user.customeraccount.current_balance -= user_bet.user_win
                    else:
                        user_event = user_bet.events.first()
                        if result.total_score == user_event.short_name:
                            user_bet.user.customeraccount.current_balance += user_bet.user_win
                            user_bet.is_went = True
                        else:
                            user_bet.is_went = False
                            user_bet.user.customeraccount.current_balance -= user_bet.user_win

                    user_bet.save()
                    user_bet.user.customeraccount.save()


@app.task
def update_type_for_user_bets():
    user_bets = UserBet.objects.filter(is_went=None).all()
    for user_bet in user_bets:
        event = user_bet.events.first()
        if event:
            match = event.match_set.first()
            if match:
                if match.request_type == 'live':
                    user_bet.bet_type = 'live'
                    user_bet.save()


@app.task
def update_additional_events_to_matches_live():
    matches = Match.objects.filter(request_type='live', deleted=False, ended=False).all()
    for match in matches:
        current_match_api = CurrentMatchWrapper(request_type=match.request_type, game_id=match.game_num, uniq=match.uniq)
        current_match_api.update_addition_events_matches(match)


@app.task
def update_additional_events_to_matches_line():
    matches = Match.objects.filter(request_type='line', deleted=False, ended=False).all()
    for match in matches:
        current_match_api = CurrentMatchWrapper(request_type=match.request_type, game_id=match.game_num, uniq=match.uniq)
        current_match_api.update_addition_events_matches(match)



