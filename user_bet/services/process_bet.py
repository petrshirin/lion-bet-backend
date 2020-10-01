from user_bet.models import *
from rest_framework.request import Request
from typing import List, \
    Dict, Union
from user_bet.go_bet_api_wrapper import GoBetWrapper
import logging
from sport_events.models import MatchEvent


def process_bet_status(request: Request) -> bool:
    bets = request.data['Heads']
    if bets:
        return False
    for bet in bets:
        user_bet = UserBet.objects.filter(bet_code=bet['KeyHead']['BarCode']).first()
        if not user_bet:
            return False
        status = request.data['Status']
        exit_code = request.data['ExtStatus']
        if status == 2 and exit_code == 0:
            user_bet.user.customeraccount.current_balance += user_bet.user_win
            user_bet.is_went = True
            user_bet.save()
            user_bet.user.customeraccount.save()
        elif status == 4 and exit_code == 0:
            user_bet.user.customeraccount.current_balance -= user_bet.user_win
            user_bet.is_went = True
            user_bet.save()
            user_bet.user.customeraccount.save()
        elif status == 2 and exit_code == 1:
            user_bet.user.customeraccount.current_balance += user_bet.user_bet
            user_bet.is_went = True
            user_bet.save()
            user_bet.user.customeraccount.save()
        else:
            return False








