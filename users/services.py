from .models import *
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from typing import Optional, List, \
    Dict, Any, Union
from rest_framework.request import Request
from .serializers import ClientInfoSerializer, ClientRegisterSerializer, \
    ChangePasswordSerializer, ChangeClientInfoSerializer
from .Exceptions import UniqueUser
from django.db.models.query import Q
from rest_framework.authtoken.models import Token


def get_self_info_client(request: Request) -> ReturnDict:
    """
    Get info about current User
    It do not work if user not authorized
    :param request:
    :return:
    """
    client_info_serializer = ClientInfoSerializer(request.user.client)
    return client_info_serializer.data


def register_client(request: Request) -> Dict:
    """
    This controller get data in request and register new user.
    If user was created successfully - return info about current user with id
    :param request:
    :return:
    """
    try:
        check_password(request.data.get('password1'), request.data.get('password2'))
    except ValueError as err:
        return {'errors': str(err), 'success': False}

    try:
        check_user_from_db(request.data.get('username'), request.data.get('email'))
    except UniqueUser as err:
        return {'errors': str(err), 'success': False}

    ser = ClientRegisterSerializer(data=request.data)
    if ser.is_valid():
        try:
            user = User.objects.create_user(username=request.data.get('username'),
                                            password=request.data.get('password1'),
                                            email=ser.data['email'])
            Client.objects.create(**ser.validated_data, user=user)

        except Exception as err:
            return {'errors': str(err), 'success': False}
        key = generate_token(user)
        if key is not None:
            return {'data': ser.data, 'success': True, 'key': key}
        else:
            return {'data': ser.data, 'success': False,
                    'errors': "token does not generated, need to use login form"}
    else:
        return {'errors': ser.errors, 'success': False}


def change_password(request: Request) -> Dict:
    """
    Check both password in request and change it in authorized user
    :param request:
    :return:
    """
    ser = ChangePasswordSerializer(data=request.data)
    if ser.is_valid():
        try:
            check_password(ser.validated_data['password1'], ser.validated_data['password2'])
        except ValueError as err:
            return {'errors': err, 'success': False}
        request.user.set_password(ser.validated_data['password1'])
        return {'data': 'ok', 'success': True}
    else:
        return ser.errors


def change_client_info(request: Request) -> Dict:
    """
    get data in request and change info in current Client
    :param request:
    :return:
    """
    ser = ChangeClientInfoSerializer(data=request.data)
    if ser.is_valid():
        ser.update(request.user.client, validated_data=ser.validated_data)
        return {'data': 'ok', 'success': True}
    else:
        return {'errors': ser.errors, 'success': True}


def check_user_from_db(username: str, email: str) -> bool:
    """
    function check username in db
    if username or email are not unique - raise Exception UniqueUser
    :param email:
    :param username:
    :return: True
    """
    if User.objects.filter(Q(username=username) | Q(email=email)).first():
        raise UniqueUser("user already exist")
    else:
        return True


def check_password(password1: str, password2: str) -> bool:
    """
    Check two password on match or raise Exception ValueError
    :param password1:
    :param password2:
    :return: True
    """
    if password1 == password2:
        return True
    else:
        raise ValueError('Passwords do not match')


def generate_token(user: User) -> Union[str, None]:
    token = Token.objects.create(user=user)
    if token.created:
        return token.key
    else:
        return None


