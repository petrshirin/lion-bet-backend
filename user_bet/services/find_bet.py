from user_bet.models import *
from rest_framework.request import Request
from typing import List, \
    Dict, Union
from user_bet.go_bet_api_wrapper import GoBetWrapper
import logging
from sport_events.models import MatchEvent
from django.conf import settings
from user_bet.serializers import UserBetSerializers
from rest_framework.serializers import ReturnList


def get_users_bet(user: User) -> Dict:
    bets = UserBet.objects.filter(user=user, deleted=False).all()
    bets_ser = UserBetSerializers(bets, many=True)
    return {"data": bets_ser.data, 'success': True}


def get_bet_on_ticket(user: User, ticket: str) -> Dict:
    bet = UserBet.objects.filter(user=user, deleted=False, bet_code=ticket).first()
    if not bet:
        return {"errors": "Ставка не найдена", 'success': False}
    bets_ser = UserBetSerializers(bet)
    return {"data": bets_ser.data, 'success': True}

