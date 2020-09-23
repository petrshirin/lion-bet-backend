from celery.task import periodic_task
from celery.schedules import crontab
from .betapi_wrapper import SportWrapper, CountryWrapper, TournamentWrapper, MatchWrapper, CurrentMatchWrapper, Match
from celery import Celery
from lion_bet_backend.celery import app
import logging


LOG = logging.getLogger(__name__)


@app.task
def update_countries_line():
    country_api = CountryWrapper()
    country_api.delete_all_from_db()
    country_api.save_items_to_db()
    LOG.info('update line countries completed')


@app.task
def update_tournaments_line():
    tournament_api = TournamentWrapper()
    tournament_api.delete_all_from_db()
    tournament_api.save_items_to_db()
    LOG.info('update line tournaments completed')


@app.task
def update_matches_line():
    matches_api = MatchWrapper()
    matches_api.delete_all_from_db()
    matches_api.save_items_to_db()
    LOG.info('update line matches completed')


@app.task
def update_countries_live():
    country_api = CountryWrapper('live')
    country_api.delete_all_from_db()
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
    for match in Match.objects.filter(deleted=False, ended=False):
        current_match_api = CurrentMatchWrapper(game_id=match.game_num)
        result = current_match_api.close_current_match()
        if not result:
            match.ended = True
            match.save()






