import requests
from json import JSONDecodeError
import logging
from typing import Union, List, Dict
from django.conf import settings
import json

MAKE_BET_PARTNER_ID = int(settings.MAKE_BET_PARTNER_ID)
MAKE_BET_API_URL = settings.MAKE_BET_API_URL
REMOTE_HOST = settings.REMOTE_HOST
PARTNER_MAIL = settings.GO_BET_EMAIL

LOG = logging.getLogger(__name__)


class GoBetWrapper(object):

    def __init__(self):
        self.partner_id = MAKE_BET_PARTNER_ID
        self.url = MAKE_BET_API_URL
        self.currency = 'RUB'
        self.cookies = ""

    def register_user(self, email: str, password: str, phone: str) -> bool:
        """
        Register new user in GO BET API service
        :param email: login
        :param password: password to authorize
        :param phone: additional info about user
        :return: True/False
        """
        data = {
            "registerModel": {
                "Email": email,
                "Password": password,
                "registr_phone": phone,
                "currency": self.currency,
                "partner": self.partner_id
            }
        }
        response = requests.post(f'{self.url}/WebServices/Mobile/BetsStoreService.asmx/Register/', json=data)
        try:
            result = response.json()
            if result['d']['IsError']:
                LOG.error(f"Register user error: {result['d']['ErrorCodes']}")
                return False
            return True
        except JSONDecodeError as err:
            LOG.error(f"Register user error in json(): {str(err)}")
            return False

    def authorize_user(self, email: str, password: str) -> Union[int, None]:
        """
        Authorize user on email and password and save cookies in class property
        :param email:
        :param password:
        :return: user_id in system or None
        """
        data = {
            "login": email,
            "password": password
        }
        response = requests.post(f'{self.url}/WebServices/BCService.asmx/LogIn/', json=data)
        try:
            result = response.json()
            if not result['d']:
                LOG.error(f"Authorize user error, user not register")
                return None
            print(result)
            self.cookies = response.cookies
            return result['d']['UserId']
        except JSONDecodeError as err:
            LOG.error(f"Register user error in json(): {str(err)}")
            return None

    def get_current_bet(self, email, barcode):
        data = {
            "login": email,
            "links": [barcode]
        }

        LOG.debug(data)
        response = requests.post(f"{self.url}/loadbars/", json=data, cookies=self.cookies)
        if response.ok:
            try:
                start_json = response.text.find('{')
                return json.loads(response.text[start_json:])

            except JSONDecodeError as err:
                print(response.text)
                LOG.error(f"Make bet error in json(): {str(err)}")
                return None

    def make_bet(self, bets_list: List, amount: float, rate_mode: str = 'accept') -> Union[Dict, None]:
        """
        do request to go bet service and start to get updates in remote host

        :param bets_list:
        :param amount:
        :param rate_mode:
        :return: None/Dict with bet info
        """
        data = {
            "data": {
                "list_bets": bets_list,
                "realAmount": amount,
                "currency": self.currency,
                "remote_host": REMOTE_HOST,
                "lang": 'ru',
                "rate_mode": rate_mode
            }
        }
        LOG.debug(data)
        response = requests.post(f"{self.url}/bet/place/", json=data, cookies=self.cookies)

        if response.ok:
            try:
                start_json = response.text.find('{')
                result = json.loads(response.text[start_json:])
                if result['errorCode']:
                    LOG.error(data)
                    LOG.error(f"make bet error: {result['fullErrorCode']} {result['errorMessage']}")
                return result
            except JSONDecodeError as err:
                print(response.text)
                LOG.error(f"Make bet error in json(): {str(err)}")
                return None

    def get_bet_status(self, bet_code: str) -> Union[Dict, None]:
        """

        :param bet_code:
        :return:
        """
        data = {
            'mails': [PARTNER_MAIL],
            'links': [bet_code],
            "mode": "mixed"
        }
        LOG.debug(data)
        response = requests.post(f"{self.url}/loadbars/", json=data, cookies=self.cookies)
        if response.ok:
            try:
                result = response.json()
                if result.get('errorCode'):
                    LOG.error(data)
                    return None
                return result[0]
            except JSONDecodeError as err:
                LOG.error(f"Make bet error in json(): {str(err)}")
                return None
