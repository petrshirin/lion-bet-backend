from user_bet.models import *
from rest_framework.request import Request
from typing import List, \
    Dict, Union
from user_bet.go_bet_api_wrapper import GoBetWrapper
import logging
from sport_events.models import MatchEvent
from django.conf import settings

LOG = logging.getLogger(__name__)


def process_bet_status(data: dict) -> bool:
    bets = data.get('Heads')
    if not bets:
        LOG.error('error in bets')
        LOG.error(data)
        return False
    result = True
    for bet in bets:
        user_bet = UserBet.objects.filter(bet_code=bet['KeyHead']['BarCode']).first()
        if not user_bet:
            LOG.error('error in find this bet')
            LOG.error(data)
            result = False
            continue
        status = bet.get('Status')
        exit_code = bet.get('ExtStatus', 0)
        LOG.error(status, exit_code)
        if status == 2 and exit_code == 0:
            user_bet.user.customeraccount.current_balance += user_bet.user_win
            user_bet.is_went = True
            user_bet.save()
            user_bet.user.customeraccount.save()
            LOG.error(data)
        elif status == 4 and exit_code == 0:
            if user_bet.is_went:
                user_bet.user.customeraccount.current_balance -= user_bet.user_win
                user_bet.user.customeraccount.save()
            user_bet.is_went = False
            user_bet.save()
            LOG.error(data)
        elif status == 2 and exit_code == 1:
            user_bet.user.customeraccount.current_balance += user_bet.user_bet
            user_bet.is_went = False
            user_bet.returned = True
            user_bet.save()
            user_bet.user.customeraccount.save()
            LOG.error(data)
        else:
            LOG.error('error in status bet')
            LOG.error(data)
            result = False
    return result


def calculate_lost_bets(bets_list):
    wrapper = GoBetWrapper()
    wrapper.authorize_user(settings.GO_BET_EMAIL, settings.GO_BET_PASSWORD)
    for bet in bets_list:
        response = wrapper.get_bet_status(bet.bet_code)
        if response:
            process_bet_status(response)







