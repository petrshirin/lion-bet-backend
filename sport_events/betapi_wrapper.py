import requests
from .models import *
from django.db.models.query import QuerySet
from typing import Union, Dict, Any
from django.db.utils import IntegrityError
from datetime import datetime
import logging

BASE_PATH = 'https://odds.incub.space'
API_SECRET_KEY = 'Test_7_Iskander_ekf3kfkdsjh4'

LOG = logging.getLogger(__name__)


class BetApiWrapper(object):
    """
    Abstract class to wrap requests to bet api
    """

    def __init__(self, request_type: str = 'line', lang: str = 'ru'):
        """
        Create params to do clear request
        :param request_type: line or life
        :param lang: ru or en
        """
        self.request_type = request_type
        self.lang = lang
        self.api_version = 'v1'
        self.headers = {'Package': API_SECRET_KEY}
        self.url = f'{BASE_PATH}/{self.api_version}'

    def _do_request(self) -> Union[Dict, None]:
        pass

    @staticmethod
    def get_all_db_items() -> QuerySet:
        """
        get all items from db and return QuerySet
        :return:
        """
        pass

    def save_items_to_db(self) -> None:
        """
        save all items from request to db
        :return:
        """
        pass


class SportWrapper(BetApiWrapper):

    def __init__(self, request_type: str = 'line', lang: str = 'ru'):
        super(SportWrapper, self).__init__(request_type, lang)

    def _do_request(self) -> Union[Dict, None]:
        """
        do request to bet api and get all sport to json format
        :return:
        """
        response = requests.get(f'{self.url}/sports/{self.request_type}/{self.lang}', headers=self.headers)
        if response.ok:
            return response.json()
        else:
            return None

    @staticmethod
    def get_all_db_items() -> QuerySet:
        """
        get all sport from db and return QuerySet
        :return:
        """
        sports = Sport.objects.all()
        return sports

    def save_items_to_db(self) -> None:
        """
        save all sport from request to db
        :return:
        """
        sports = self._do_request()
        if sports:
            for sport in sports['body']:
                if not Sport.objects.filter(api_id=sport.get('id')).first():
                    Sport.objects.create(api_id=sport.get('id'),
                                         name=sport.get('name'),
                                         name_en=sport.get('name_en'))


class CountryWrapper(BetApiWrapper):

    def __init__(self, request_type: str = 'line', lang: str = 'ru', sport_id: int = 0):
        """
        get all countries of some sport
        :param request_type:
        :param lang:
        :param sport_id: if 0, get all countries
        """
        super(CountryWrapper, self).__init__(request_type, lang)
        self.sport_id = sport_id

    def _do_request(self) -> Union[Dict, None]:
        """
        do request to bet api and get all countries to json format
        :return:
        """
        response = requests.get(f'{self.url}/countries/{self.sport_id}/{self.request_type}/{self.lang}', headers=self.headers)
        if response.ok:
            return response.json()
        else:
            return None

    def get_all_db_items(self) -> QuerySet:
        """
        get all countries from db and return QuerySet
        :return:
        """
        if self.sport_id:
            countries = Country.objects.filter(sport_id=self.sport_id).all()
        else:
            countries = Country.objects.all()
        return countries

    def save_items_to_db(self) -> None:
        """
        save all countries from request to db
        :return:
        """
        items = self._do_request()
        if items:
            for country in items['body']:
                if not Country.objects.filter(api_id=country.get('id')).first():
                    try:
                        sport = Sport.objects.get(api_id=country.get('sport_id'))
                        Country.objects.create(api_id=country.get('id'),
                                               name=country.get('name'),
                                               name_en=country.get('name_en'),
                                               sport=sport)
                    except Sport.DoesNotExist:
                        LOG.debug(f"SPORT_ID: {country.get('sport_id')}")
                        continue


class TournamentWrapper(BetApiWrapper):

    def __init__(self,
                 request_type: str = 'line',
                 lang: str = 'ru',
                 sport_id: int = 0,
                 country_id: int = 0):
        """
        get all countries of some sport and some country
        :param request_type:
        :param lang:
        :param sport_id: if 0, ignored argument
        :param country_id:  if 0, ignored argument
        """
        super(TournamentWrapper, self).__init__(request_type, lang)
        self.sport_id = sport_id
        self.country_id = country_id

    def _do_request(self) -> Union[Dict, None]:
        """
        do request to bet api and get all tournaments to json format
        :return:
        """
        response = requests.get(f'{self.url}/tournaments/{self.sport_id}/{self.country_id}/{self.request_type}/{self.lang}', headers=self.headers)
        if response.ok:
            return response.json()
        else:
            return None

    def get_all_db_items(self) -> QuerySet:
        """
        get all countries from db and return QuerySet
        :return:
        """
        if self.sport_id or self.country_id:
            if self.sport_id and self.country_id:
                tournaments = Tournament.objects.filter(sport_id=self.sport_id,
                                                        country_id=self.country_id).all()
            elif self.sport_id:
                tournaments = Tournament.objects.filter(sport_id=self.sport_id).all()

            else:
                tournaments = Tournament.objects.filter(country_id=self.country_id).all()
        else:
            tournaments = Tournament.objects.all()
        return tournaments

    def save_items_to_db(self) -> None:
        """
        save all countries from request to db
        :return:
        """
        items = self._do_request()
        if items:
            for tournament in items['body']:
                if not Tournament.objects.filter(api_id=tournament.get('id')).first():
                    try:
                        sport = Sport.objects.get(api_id=tournament.get('sport_id'))
                        country = Country.objects.get(api_id=tournament.get('country_id'))
                        Tournament.objects.create(api_id=tournament.get('id'),
                                                  name=tournament.get('name'),
                                                  name_en=tournament.get('name_en'),
                                                  sport=sport,
                                                  country=country)
                    except Sport.DoesNotExist:
                        LOG.error(f"SPORT_ID: {tournament.get('sport_id')}")
                        continue
                    except Country.DoesNotExist:
                        LOG.error(f"COUNTRY_ID: {tournament.get('country_id')}")
                        continue


class MatchWrapper(BetApiWrapper):

    def __init__(self,
                 request_type: str = 'line',
                 lang: str = 'ru',
                 sport_id: int = 0,
                 country_id: int = 0):
        """
        get all countries of some sport and some country
        :param request_type:
        :param lang:
        :param sport_id: if 0, ignored argument
        :param country_id:  if 0, ignored argument
        """
        super(MatchWrapper, self).__init__(request_type, lang)
        self.sport_id = sport_id
        self.country_id = country_id

    def _do_request(self) -> Union[Dict, None]:
        """
        do request to bet api and get all events to json format
        :return:
        """
        response = requests.get(f'{self.url}/events/{self.sport_id}/{self.country_id}/sub/1000/{self.request_type}/{self.lang}', headers=self.headers)
        if response.ok:
            return response.json()
        else:
            return None

    def get_all_db_items(self) -> QuerySet:
        """
        get all countries from db and return QuerySet
        :return:
        """
        if self.sport_id or self.country_id:
            if self.sport_id and self.country_id:
                matches = Match.objects.filter(sport_id=self.sport_id,
                                               country_id=self.country_id).all()
            elif self.sport_id:
                matches = Match.objects.filter(sport_id=self.sport_id).all()

            else:
                matches = Match.objects.filter(country_id=self.country_id).all()
        else:
            matches = Match.objects.all()
        return matches

    def save_items_to_db(self) -> None:
        """
        save all countries from request to db
        :return:
        """
        items = self._do_request()
        if items:
            for tournament in items['body']:
                for match in tournament['events_list']:
                    if not Match.objects.filter(uniq=match.get('uniq')).first():
                        try:
                            sport = Sport.objects.get(api_id=match.get('sport_id'))
                            tor = Tournament.objects.get(api_id=match.get('tournament_id'))
                            new_match = Match.objects.create(game_num=match.get('game_num'),
                                                             sport=sport,
                                                             tournament=tor,
                                                             game_start=datetime.fromtimestamp(match.get('game_start')),
                                                             opp_1_name=match.get('opp_1_name'),
                                                             opp_2_name=match.get('opp_2_name'),
                                                             opp_1_id=match.get('opp_1_id'),
                                                             opp_2_id=match.get('opp_2_id'))
                        except Sport.DoesNotExist:
                            LOG.error(f"SPORT_ID: {match.get('sport_id')}")
                            continue
                        except Tournament.DoesNotExist:
                            LOG.error(f"TOURNAMENT_ID: {match.get('tournament_id')}")
                            continue
                                
                        for event in match.get('game_oc_list'):
                            new_event = MatchEvent.objects.create(oc_group_name=event['oc_group_name'],
                                                                  oc_name=event['oc_name'],
                                                                  oc_rate=event['oc_rate'],
                                                                  oc_pointer=event['oc_pointer'])
                            new_match.events.add(new_event)


