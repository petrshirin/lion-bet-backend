from typing import Optional, List, \
    Dict, Any, Union
from rest_framework.request import Request
from django.db.models.query import Q
import logging
from rest_framework.serializers import ReturnList
from users.serializers import Client, CustomerAccount, CustomerAccountSerializer, ClientInfoSerializer
from user_bet.serializers import UserBet, UserBetSerializers
from user_payment.serializers import UserMoneyRequestSerializer, UserMoneyRequest
from techsupport.serializers import ClientRequestSerializer, ClientRequest

def get_user_list(page: int = 0) -> ReturnList:

    start_user = 10 * page
    end_user = start_user + 10

    users = Client.objects.filter(user__is_active=True).all()[start_user:end_user]
    users_ser = ClientInfoSerializer(users, many=True)
    data = users_ser.data
    for i in range(len(users)):
        data[i]['customer_account'] = CustomerAccountSerializer(users[i].user.customeraccount).data
    return data


def edit_user(request: Request) -> Dict:
    client_ser = ClientInfoSerializer(data=request.data)
    if client_ser.is_valid():
        try:
            client_ser.update(Client.objects.get(pk=client_ser.validated_data['id']), client_ser.validated_data)
            return {'data': 'ok', 'success': True}
        except Client.DoesNotExist:
            return {'errors': "Пользователь не найден", 'success': False}
    else:
        return {'errors': client_ser.errors, 'success': False}


def delete_user(user_id: int) -> Dict:
    client = Client.objects.filter(pk=user_id).first()
    if not client:
        return {'errors': "Пользователь не найден", 'success': False}
    client.user.is_active = False
    client.user.save()


def block_customer_account(user_id: int) -> Dict:
    client = Client.objects.filter(pk=user_id).first()
    if not client:
        return {'errors': "Пользователь не найден", 'success': False}
    client.user.customeraccount.blocked = True
    client.user.customeraccount.save()


def get_user_bets(user_id: int) -> Dict:
    client = Client.objects.filter(pk=user_id).first()
    if not client:
        return {'errors': "Пользователь не найден", 'success': False}
    user_bets = UserBet.objects.filter(user=client.user).all()
    user_bets_ser = UserBetSerializers(user_bets, many=True)
    return {'data': user_bets_ser.data, "success": True}


def get_user_payments(user_id: int) -> Dict:
    client = Client.objects.filter(pk=user_id).first()
    if not client:
        return {'errors': "Пользователь не найден", 'success': False}

    user_payments = UserMoneyRequest.objects.filter(user=client.user).all()
    user_payments_ser = UserMoneyRequestSerializer(user_payments, many=True)
    return {'data': user_payments_ser.data, "success": True}


def get_user_tech_requests(user_id: int) -> Dict:
    client = Client.objects.filter(pk=user_id).first()
    if not client:
        return {'errors': "Пользователь не найден", 'success': False}
    user_requests = ClientRequest.objects.filter(user=client.user).all()
    user_requests_ser = ClientRequestSerializer(user_requests, many=True)
    return {'data': user_requests_ser.data, "success": True}







