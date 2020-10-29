import logging
from typing import Dict

from rest_framework.request import Request

from .models import *
from .qiwi_wrapper import QiwiWrapper
from user_bet.services.make_bet import check_balance
from .serializers import UserMoneyRequestSerializer

LOG = logging.getLogger(__name__)


def make_input_request(request: Request) -> Dict:
    wrapper = QiwiWrapper()
    if request.user.customeraccount.blocked:
        return {"errors": "Ваш счет заблокирован", "success": False}
    if request.data.get('amount'):
        try:
            amount = float(request.data.get('amount'))

            if amount < 500:
                return {"errors": "Минимальная сумма должна быть 500 рублей", "success": False}

            url = wrapper.create_form(amount)
            if url:
                UserMoneyRequest.objects.create(user=request.user, amount=amount, build=wrapper.build)
            return {"data": {'url': url}, "success": True}
        except ValueError as e:
            LOG.error(e)
    return {"errors": "Неправильная ввод", "success": False}


def make_output_request(request: Request) -> Dict:
    if request.user.customeraccount.blocked:
        return {"errors": "Ваш счет заблокирован", "success": False}

    if not request.data.get('account_number', None):
        return {"errors": "Номер счета не указан", "success": False}

    if request.data.get('amount'):
        try:
            amount = float(request.data.get('amount'))
            if UserMoneyRequest.objects.filter(user=request.user, request_type='input', accepted=True).count() < 10:
                return {"errors": "Недостаточное количество пополнений для вывода (должно быть 10 пополнений)", "success": False}
            if not check_balance(request.user, amount):
                return {"errors": "Недостаточно средств для вывода", 'success': False}
            UserMoneyRequest.objects.create(user=request.user,
                                            amount=amount,
                                            request_type='output',
                                            method=request.data.get('method', None),
                                            account_number=request.data.get('account_number', None))
            return {"data": 'ok', "success": True}
        except ValueError as e:
            LOG.error(e)
            return {"errors": "Неправильная ввод", "success": False}
        except Exception as e:
            LOG.error(e)
            return {"errors": "Не удалось создать запрос, обратитесь к администратору", "success": False}
    else:
        return {"errors": "Сумма не указана", "success": False}


def user_output_requests(user: User) -> Dict:
    user_requests = UserMoneyRequest.objects.filter(request_type='output', user=user).all()
    user_requests_ser = UserMoneyRequestSerializer(user_requests, many=True)
    return {"data": user_requests_ser.data, "success": True}


def user_input_requests(user: User) -> Dict:
    user_requests = UserMoneyRequest.objects.filter(request_type='input', user=user).all()
    user_requests_ser = UserMoneyRequestSerializer(user_requests, many=True)
    return {"data": user_requests_ser.data, "success": True}

