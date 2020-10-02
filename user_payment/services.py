import logging
from typing import Dict

from rest_framework.request import Request

from .models import *
from .qiwi_wrapper import QiwiWrapper
from user_bet.services.make_bet import check_user_balance

LOG = logging.getLogger(__name__)


def make_input_request(request: Request) -> Dict:
    wrapper = QiwiWrapper()
    if request.user.customeraccount.blocked:
        return {"errors": "Ваш счет заблокирова", "success": False}
    if request.data.get('amount'):
        try:
            amount = float(request.data.get('amount'))
            url = wrapper.create_form(amount)
            if url:
                UserMoneyRequest.objects.create(user=request.user, amount=amount, build=wrapper.build)
            return {"data": {'url': url}, "success": True}
        except ValueError as e:
            LOG.error(e)
    return {"errors": "Неправильная ввод", "success": False}


def make_output_request(request: Request) -> Dict:
    if request.user.customeraccount.blocked:
        return {"errors": "Ваш счет заблокирова", "success": False}
    if request.data.get('amount'):
        try:
            amount = float(request.data.get('amount'))
            if UserMoneyRequest.objects.filter(user=request.user, request_type='input', accepted=True).count() < 5:
                return {"errors": "Недостаточное количество пополнений для вывода", "success": False}
            if check_user_balance(request.user, amount):
                return {"errors": "Недостаточно средств для вывода", 'success': False}
            UserMoneyRequest.objects.create(user=request.user, amount=amount, request_type='output')
            return {"data": 'ok', "success": True}
        except ValueError as e:
            LOG.error(e)
            return {"errors": "Неправильная ввод", "success": False}
        except Exception as e:
            LOG.error(e)
            return {"errors": "Не удалось создать запрос, обратитесь к администратору", "success": False}
    else:
        return {"errors": "Сумма не указана", "success": False}
