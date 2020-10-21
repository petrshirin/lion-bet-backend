from user_bet.models import *
from rest_framework.request import Request
from typing import List, \
    Dict, Union
from user_bet.go_bet_api_wrapper import GoBetWrapper
import logging
from sport_events.models import MatchEvent
from django.conf import settings
from user_bet.serializers import UserBetSerializers
from random import choice
import string

LOG = logging.getLogger(__name__)


ERROR_RU = {
    '|error_exist_bet|': 'Такого исхода больше нет',
    '|error_repeat_bet_data|': 'Ставки из одного матча на разные ивенты',
    '|error_block_bet_data|': 'На данный момент ставка временно заблокирована для приема.'
}


def make_bet(request: Request, bet_type: str) -> Dict:
    validated_data = _validate_bet_request_data(request.data)

    if request.user.customeraccount.blocked:
        LOG.info(f'customer account is blocked')
        return {"errors": "Ваш счет заблокирован", "success": False}

    if validated_data.get('errors'):
        return validated_data

    events = bet_ids_to_models(validated_data['bets_ids'])
    amount = validated_data['amount']
    if events is None:
        return {'errors': "Неверный ID Ставки", 'success': False}

    if check_admin_bet(events):
        if len(events) == 1:
            new_model_bet = _save_bet_to_db(user=request.user, new_bet={'BetCode': ''.join(choice(string.ascii_lowercase) for i in range(8)),
                                                                        'd': {"BetHeadDetail": {"Coef": events[0].oc_rate,
                                                                                                "PosWin": amount * float(events[0].oc_rate),
                                                                                                'BetCode': ''.join(choice(string.ascii_lowercase) for i in range(8))
                                                                                                }
                                                                              }
                                                                        },
                                            bet_type=bet_type, amount=amount)
            if not new_model_bet:
                LOG.error(f'error in save bet')
                return {"errors": f"Ошибка при создании ставки", 'success': False}
            model_bet = _add_to_model_events(new_model_bet, events)
            if not model_bet:
                new_model_bet.delete()
                LOG.error(f'error in save bet events')
                return {"errors": f"Ошибка при создании ставки, Ошибка в ивентах", 'success': False}
            bet_ser = UserBetSerializers(new_model_bet)
            return {"data": bet_ser.data, "success": True}
        else:
            return {"errors": f"Одна или несколько ставок недоступны, для экспресса", 'success': False}

    if not check_balance(request.user, amount):
        return {"errors": "Недостаточно средств для совершения операции", 'success': False}

    list_bets = _create_list_bets(events, bet_type)

    if not list_bets:
        return {"errors": "Одна из ставок с ошибкой", 'success': False}

    new_bet = _do_request_to_go_bet(list_bets, amount)
    if not new_bet:
        return {"errors": "Неизвестная ошибка при создании ставки", 'success': False}
    if new_bet.get('errorCode'):
        return {"errors": f"Ошибка при создании ставки {ERROR_RU.get(new_bet.get('errorMessage'))}", 'success': False}
    new_model_bet = _save_bet_to_db(request.user, new_bet, bet_type, amount)
    if not new_model_bet:
        return {"errors": f"Ошибка при создании ставки {ERROR_RU.get(new_bet.get('errorMessage'))}", 'success': False}
    model_bet = _add_to_model_events(new_model_bet, events)
    if not model_bet:
        new_model_bet.delete()
        return {"errors": f"Ошибка при создании ставки, Ошибка в ивентах", 'success': False}
    bet_ser = UserBetSerializers(new_model_bet)
    request.user.customeraccount.current_balance = float(request.user.customeraccount.current_balance) - float(new_model_bet.user_bet)
    request.user.customeraccount.save()
    return {"data": bet_ser.data, "success": True}


def bet_ids_to_models(bets_ids: List[int]) -> Union[List, None]:
    events = []
    for bet_id in bets_ids:
        try:
            event = MatchEvent.objects.get(pk=bet_id)
            events.append(event)
        except MatchEvent.DoesNotExist:
            LOG.error("Invalid event id")
            return None
    return events


def _create_bet_str(event: MatchEvent, bet_type: str) -> str:
    return f"{bet_type}#{event.oc_pointer}#{event.oc_rate}"


def _validate_bet_request_data(data: Request.data) -> Dict:

    if data.get('bets_ids') and isinstance(data.get('bets_ids'), list):
        bets_ids = data.get('bets_ids')
    else:
        return {"errors": "Список id не существует или пустой", 'success': False}
    if data.get('amount'):
        amount = float(data.get('amount'))
    else:
        return {"errors": "Суммы сделки не существует или пустая", 'success': False}

    return {"bets_ids": bets_ids, "amount": amount}


def _create_list_bets(events: List[MatchEvent], bet_type: str) -> Union[List[str], None]:
    list_bets = []
    for event in events:
        bet = _create_bet_str(event, bet_type)
        if bet:
            list_bets.append(bet)
        else:
            return None
    return list_bets


def _do_request_to_go_bet(list_bets: List, amount) -> Union[Dict, None]:
    wrapper = GoBetWrapper()
    wrapper.authorize_user(settings.GO_BET_EMAIL, settings.GO_BET_PASSWORD)
    return wrapper.make_bet(list_bets, amount)


def _save_bet_to_db(user: User, new_bet: Dict, bet_type: str, amount: float) -> Union[UserBet, None]:
    print(new_bet)
    try:
        new_model_bet = UserBet.objects.create(user=user,
                                               bet_type=bet_type,
                                               bet_code=new_bet['d']['BetHeadDetail']['BetCode'],
                                               win_coefficient=new_bet['d']['BetHeadDetail']['Coef'],
                                               user_bet=amount,
                                               user_win=new_bet['d']['BetHeadDetail']['PosWin'])
    except Exception as e:
        LOG.error(e)
        return None

    return new_model_bet


def _add_to_model_events(new_model_bet: UserBet, events: List[UserBet]) -> Union[UserBet, None]:
    try:
        for event in events:
            new_model_bet.events.add(event)
        new_model_bet.save()
    except Exception as e:
        LOG.error(e)
        return None
    return new_model_bet


def check_balance(user: User, amount: float) -> bool:
    return float(user.customeraccount.current_balance) >= amount


def check_admin_bet(events: List[MatchEvent]) -> bool:
    if len(events) == 1:
        return events[0].admin_created
    for event in events:
        if event.admin_created:
            return True
    return False
