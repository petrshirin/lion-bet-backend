from celery.task import periodic_task
from celery.schedules import crontab
from .betapi_wrapper import SportWrapper, CountryWrapper, TournamentWrapper, MatchWrapper
from celery import Celery
from lion_bet_backend.celery import app
import logging


LOG = logging.getLogger(__name__)


app.conf.beat_schedule = {
    "update_sports_line": {
        'task': 'tasks.update_sports_line',
        'schedule': crontab(hour=23),
    },
    "update_countries_line": {
            'task': 'tasks.update_countries_line',
            'schedule': crontab(hour=23),
        },
    "update_tournaments_line": {
            'task': 'tasks.update_sports_line',
            'schedule': crontab(hour=1),
        },
    "update_matches_line": {
            'task': 'tasks.update_matches_line',
            'schedule': crontab(minute=1),
        },

}


@app.task
def update_sports():
    sport_api = SportWrapper()
    sport_api.save_items_to_db()
    LOG.info('update sports completed')


@app.task
def update_countries():
    country_api = CountryWrapper()
    country_api.save_items_to_db()
    LOG.info('update countries completed')


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
def update_tournaments_live():
    tournament_api = TournamentWrapper('live')
    tournament_api.delete_all_from_db()
    tournament_api.save_items_to_db()
    LOG.info('update live tournaments completed')


@app.task
def update_matches_live():
    matches_api = MatchWrapper('live')
    matches_api.delete_all_from_db()
    matches_api.save_items_to_db()
    LOG.info('update live matches completed')






