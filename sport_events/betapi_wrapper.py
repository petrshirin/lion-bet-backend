import requests
from .models import *
from django.db.models.query import QuerySet
from typing import Union, Dict, Any
from datetime import datetime, timezone, timedelta
import logging
from django.conf import settings
from django.db.utils import IntegrityError


BASE_PATH = settings.BET_API_HOST
API_SECRET_KEY = settings.BET_API_SECRET_KEY
tz = timezone(timedelta(hours=3), name=settings.TIME_ZONE)

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

    @staticmethod
    def check_response_for_active_token(resp: Dict) -> bool:
        if resp['body'] == 'Error in you package!' or resp['body'] == 'Your package life has expired!':
            LOG.error(f"{resp['body']} {datetime.utcnow()}")
            return False
        return True


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
            json_resp = response.json()
            if self.check_response_for_active_token(json_resp):
                return json_resp
            return None
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

    def delete_all_from_db(self) -> int:
        return Sport.objects.filter(request_type=self.request_type).delete()

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
                                         name_en=sport.get('name_en'),
                                         request_type=self.request_type)


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
            json_resp = response.json()
            if self.check_response_for_active_token(json_resp):
                return json_resp
            return None
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

    def delete_all_from_db(self) -> int:
        if self.sport_id:
            return Tournament.objects.filter(request_type=self.request_type, sport__api_id=self.sport_id).delete()
        else:
            return Tournament.objects.filter(request_type=self.request_type).delete()

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
                                               sport=sport,
                                               request_type=self.request_type)
                    except Sport.DoesNotExist:
                        LOG.debug(f"SPORT_ID: {country.get('sport_id')}")
                        continue


class TournamentWrapper(BetApiWrapper):

    def __init__(self,
                 request_type: str = 'line',
                 lang: str = 'ru',
                 sport_id: int = 0,
                 country_id: int = 0, count: int = None):
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
            json_resp = response.json()
            if self.check_response_for_active_token(json_resp):
                return json_resp
            return None
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

    def delete_all_from_db(self) -> int:
        return Tournament.objects.filter(request_type=self.request_type).delete()

    def save_items_to_db(self) -> None:
        """
        save all countries from request to db
        :return:
        """
        items = self._do_request()
        if items:
            for tournament in items['body']:
                tournament_model = Tournament.objects.filter(api_id=tournament.get('id')).first()
                try:
                    sport = Sport.objects.get(api_id=tournament.get('sport_id'))
                    country = Country.objects.get(api_id=tournament.get('country_id'))
                    if not tournament_model:

                        Tournament.objects.create(api_id=tournament.get('id'),
                                                  name=tournament.get('name'),
                                                  name_en=tournament.get('name_en'),
                                                  sport=sport,
                                                  country=country,
                                                  request_type=self.request_type)
                    else:
                        tournament_model.name = tournament.get('name')
                        tournament_model.name_en = tournament.get('name_en')
                        tournament_model.sport = sport
                        tournament_model.country = country
                        tournament_model.request_type = self.request_type
                        tournament_model.save()
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
                 country_id: int = 0, count: int = 1000):
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
        self.count = count

    def _do_request(self, sport_id: int = None) -> Union[Dict, None]:
        """
        do request to bet api and get all events to json format
        :return:
        """
        if sport_id is None:
            response = requests.get(f'{self.url}/events/{self.sport_id}/{self.country_id}/sub/{self.count}/{self.request_type}/{self.lang}', headers=self.headers)
        else:
            response = requests.get(f'{self.url}/events/{sport_id}/{self.country_id}/sub/{self.count}/{self.request_type}/{self.lang}', headers=self.headers)
        if response.ok:
            json_resp = response.json()
            if self.check_response_for_active_token(json_resp):
                return json_resp
            return None
        else:
            return None

    def delete_all_from_db(self) -> int:
        matches = Match.objects.filter(request_type=self.request_type).all()
        for m in matches:
            m.events.all().delete()
        return matches.delete()[0]

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
        all_sports_from_db = Sport.objects.all()
        items = []
        for sport_from_db in all_sports_from_db:
            tmp_items = self._do_request(sport_from_db.api_id)

            if tmp_items is None:
                return

            items += tmp_items['body']
        if items:
            for tournament in items:
                for match in tournament['events_list']:
                    old_match = Match.objects.filter(uniq=match.get('uniq')).first()
                    if not old_match:
                        try:
                            sport = Sport.objects.get(api_id=match.get('sport_id'))
                            tor = Tournament.objects.get(api_id=match.get('tournament_id'))
                            new_match = Match.objects.create(game_num=match.get('game_num'),
                                                             game_id=match.get('game_id'),
                                                             uniq=match.get('uniq'),
                                                             sport=sport,
                                                             tournament=tor,
                                                             name=f"{match.get('opp_1_name')} - {match.get('opp_2_name')}",
                                                             game_start=datetime.fromtimestamp(match.get('game_start')),
                                                             opp_1_name=match.get('opp_1_name'),
                                                             opp_2_name=match.get('opp_2_name'),
                                                             opp_1_id=match.get('opp_1_id'),
                                                             opp_2_id=match.get('opp_2_id'),
                                                             opp_1_icon=f'https://cdn.incub.space/v1/opp/icon/{match.get("opp_1_icon")}.png',
                                                             opp_2_icon=f'https://cdn.incub.space/v1/opp/icon/{match.get("opp_2_icon")}.png',
                                                             score_full=match.get('score_full'),
                                                             score_period=match.get('score_period'),
                                                             period_name=match.get('period_name'),
                                                             request_type=self.request_type,
                                                             ended=bool(match.get('finale')))
                        except Sport.DoesNotExist:
                            LOG.error(f"SPORT_ID: {match.get('sport_id')}")
                            continue
                        except Tournament.DoesNotExist:
                            LOG.error(f"TOURNAMENT_ID: {match.get('tournament_id')}")
                            continue
                        except IntegrityError:
                            LOG.error(f"Not unique match {match.get('uniq')} {old_match}")
                            continue

                        for event in match.get('game_oc_list'):

                            short_name = generate_short_name(event['oc_group_name'],
                                                             event['oc_name'],
                                                             new_match)

                            if short_name:
                                new_event = MatchEvent.objects.create(oc_group_name=event['oc_group_name'],
                                                                      oc_name=event['oc_name'],
                                                                      oc_rate=event['oc_rate'],
                                                                      oc_pointer=event['oc_pointer'],
                                                                      short_name=short_name,
                                                                      last_changed=0)
                                new_match.events.add(new_event)
                        LOG.info(f'{new_match.game_num}, events: {new_match.events.count()}')

                    else:
                        old_match.game_num = match.get('game_num')
                        old_match.game_id = match.get('game_id')
                        old_match.score_full = match.get('score_full')
                        old_match.score_period = match.get('score_period')
                        old_match.period_name = match.get('period_name')
                        old_match.request_type = self.request_type
                        old_match.game_start = datetime.fromtimestamp(match.get('game_start'))
                        old_match.ended = bool(match.get('finale'))
                        old_match.save()
                        for event in match.get('game_oc_list'):
                            is_have = False
                            for ev in old_match.events.all():
                                is_have = True
                                if ev.oc_name == event['oc_name']:
                                    ev.last_changed = 0 if ev.oc_rate == event['oc_rate'] else 1 if ev.oc_rate < event['oc_rate'] else -1
                                    ev.oc_rate = event['oc_rate']
                                    ev.oc_pointer = event['oc_pointer']

                                    ev.save()

                            if not is_have:
                                short_name = generate_short_name(event['oc_group_name'],
                                                                 event['oc_name'],
                                                                 old_match)

                                if short_name:
                                    new_event = MatchEvent.objects.create(oc_group_name=event['oc_group_name'],
                                                                          oc_name=event['oc_name'],
                                                                          oc_rate=event['oc_rate'],
                                                                          oc_pointer=event['oc_pointer'],
                                                                          short_name=short_name,
                                                                          last_changed=0)
                                    old_match.events.add(new_event)


class CurrentMatchWrapper(BetApiWrapper):

    def __init__(self,
                 request_type: str = 'line',
                 lang: str = 'ru', game_id: int = None, uniq: str = None):
        """
        get all countries of some sport and some country
        :param request_type:
        :param lang:
        :param game_id: info about match
        """
        super(CurrentMatchWrapper, self).__init__(request_type, lang)
        self.game_id = game_id
        self.uniq = uniq

    def _do_request(self) -> Union[Dict, None]:
        """
        do request to bet api and get all events to json format
        :return:
        """
        response = requests.get(f'{self.url}/event/{self.game_id}/sub/{self.request_type}/{self.lang}', headers=self.headers)
        if response.ok:
            return response.json()
        else:
            return None

    def close_current_match(self, match: Match) -> bool:

        resp = self._do_request()
        if resp:
            if isinstance(resp['body'], str):
                try:
                    match.ended = True
                    match.save()
                    return False
                except AttributeError:
                    LOG.error(f"{self.uniq, self.game_id}")
                    return False

            if resp['body'] == [] or resp['body'].get('finale', False) is True:
                try:
                    match.ended = True
                    match.save()
                    LOG.error('match closed')
                    return True
                except AttributeError:
                    LOG.error(f"{self.uniq, self.game_id}")
                    return False

    def update_addition_events_matches(self, match: Match):
        """
        update total score events
        :param match:
        :return:
        """
        response = self._do_request()

        if self.close_current_match(match):
            return

        for event_list in response['body']['game_oc_list']:
            # удалить если будут все события добавляться
            if 'Точный счет (' in event_list['group_name']:
                print('find group')
                for event in event_list['oc_list']:

                    if isinstance(event['oc_name'], str):
                        oc_name = event['oc_name'].split(' ')[-1].replace('-', ':')
                    else:
                        oc_name = event['oc_name']

                    short_name = generate_short_name(event['oc_group_name'],
                                                     oc_name,
                                                     match)
                    print(f'short_name: {short_name}')
                    old_event = match.events.filter(oc_name=oc_name).first()
                    if old_event:
                        print(f'event already')
                        old_event.last_changed = 0 if old_event.oc_rate == event['oc_rate'] else 1 if old_event.oc_rate < event['oc_rate'] else -1
                        old_event.oc_rate = event['oc_rate']
                        old_event.oc_pointer = event['oc_pointer']
                    else:
                        match_event = MatchEvent.objects.create(oc_group_name=event['oc_group_name'],
                                                                oc_name=oc_name,
                                                                oc_rate=event['oc_rate'],
                                                                oc_pointer=event['oc_pointer'],
                                                                short_name=short_name,
                                                                last_changed=0)
                        print('created ', match_event)
                        match.events.add(match_event)
                        match.save()
                break


def generate_short_name(oc_group: str, oc_name: str, match: Match) -> Union[str, None]:
    if oc_group == '1x2':
        if match.opp_1_name == oc_name:
            return 'П1'
        elif match.opp_2_name == oc_name:
            return 'П2'
        else:
            return 'X'
    elif oc_group.lower() == 'тотал':
        split_line = oc_name.split(' ')
        return f'Т{split_line[2]} {split_line[1]}'

    elif oc_group.lower() == 'индивидуальный тотал 1-го':
        split_line = oc_name.split(' ')
        if 'меньше' in oc_name.lower():
            return f'ИТМ1 {split_line[-1]}'
        elif 'больше' in oc_name.lower():
            return f'ИТБ1 {split_line[-1]}'
        else:
            return None
    elif oc_group.lower() == 'индивидуальный тотал 2-го':
        split_line = oc_name.split(' ')
        if 'меньше' in oc_name.lower():
            return f'ИТМ2 {split_line[-1]}'
        elif 'больше' in oc_name.lower():
            return f'ИТБ2 {split_line[-1]}'
        else:
            return None
    elif oc_group.lower() == 'фора':
        split_line = oc_name.split(' ')
        if match.opp_1_name in oc_name:
            return f'Ф {split_line[-1]}'
        elif match.opp_2_name in oc_name:
            return f'Ф {split_line[-1]}'
        else:
            return None
    elif oc_group.lower() == 'двойной шанс':
        if match.opp_1_name in oc_name and match.opp_2_name in oc_name:
            return f'12'
        elif match.opp_1_name in oc_name:
            return f'1X'
        elif match.opp_2_name in oc_name:
            return f'2X'
        else:
            return None
    elif oc_group.lower() == 'обе забьют':
        if 'Да' in oc_name:
            return f'Да'
        elif 'Нет' in oc_name:
            return f'Нет'
        else:
            return None
    elif 'точный счет' in oc_group.lower():
        return oc_name.split(' ')[-1].replace('-', ':')
    else:
        return None
