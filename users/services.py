from .models import *
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from typing import Optional, List, \
    Dict, Any, Union
from rest_framework.request import Request
from .serializers import ClientInfoSerializer, ClientRegisterSerializer, \
    ChangePasswordSerializer, ChangeClientInfoSerializer, CustomerAccountSerializer
from .Exceptions import UniqueUser
from django.db.models.query import Q
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
import logging


LOG = logging.getLogger(__name__)


def get_self_info_client(request: Request) -> ReturnDict:
    """
    Get info about current User
    It do not work if user not authorized
    :param request:
    :return:
    """
    client_info_serializer = ClientInfoSerializer(request.user.client)
    customer_account = CustomerAccountSerializer(request.user.customeraccount)
    data = client_info_serializer.data
    data['customer_account'] = customer_account.data
    return data


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
            client = Client.objects.create(**ser.validated_data, user=user)

        except Exception as err:
            return {'errors': str(err), 'success': False}
        key = generate_token(user)
        new_email = UserEmail(template_id=1, user=user)
        new_email.generate_code()
        is_send = send_email_to_user(1, [client.email], f'https://royal-lion.bet/activate/{new_email.code}')
        if is_send:
            new_email.save()
        if key is not None:
            return {'data': ser.data, 'success': True, 'key': key}
        else:
            return {'data': ser.data, 'success': False,
                    'errors': "Токен не сгенерирован, используйте форму логина"}
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
            if not request.user.check_password(ser.validated_data['old_password']):
                return {'errors': "Неверный старый пароль", 'success': False}
            check_password(ser.validated_data['password1'], ser.validated_data['password2'])
        except ValueError as err:
            return {'errors': str(err), 'success': False}
        request.user.set_password(ser.validated_data['password1'])
        request.user.save()
        return {'data': 'ok', 'success': True}
    else:
        return {'errors': ser.errors, 'success': False}


def change_client_info(request: Request) -> Dict:
    """
    get data in request and change info in current Client
    :param request:
    :return:
    """
    ser = ChangeClientInfoSerializer(data=request.data)
    if ser.is_valid():
        if ser.validated_data.get('email') and request.user.client.email != ser.validated_data['email']:
            request.user.client.activated = False
            new_email = UserEmail(template_id=1, user=request.user)
            new_email.generate_code()
            is_send = send_email_to_user(1, [request.user.client.email], f'http://front.ru/password/forgot/{new_email.code}')
            if is_send:
                new_email.save()
            request.user.client.save()
        ser.update(request.user.client, validated_data=ser.validated_data)
        return {'data': 'ok', 'success': True}
    else:
        return {'errors': ser.errors, 'success': False}


def check_user_from_db(username: str, email: str) -> bool:
    """
    function check username in db
    if username or email are not unique - raise Exception UniqueUser
    :param email:
    :param username:
    :return: True
    """
    if User.objects.filter(Q(username=username) | Q(email=email)).first():
        raise UniqueUser("Пользователь уже существует")
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
        raise ValueError('Пароли не совпадают')


def generate_token(user: User) -> Union[str, None]:
    token = Token.objects.create(user=user)
    if token.created:
        return token.key
    else:
        return None


def send_email_to_user(mail_type: int = 1, recipient_list: List[str] = None, email_info: str = None) -> bool:
    try:
        template = EmailTemplate.objects.get(pk=mail_type)
    except EmailTemplate.DoesNotExist:
        return False
    result = send_mail(template.subject, template.text.format(email_info), template.from_email, recipient_list)
    LOG.info(f'Email of type {mail_type} send this users: {recipient_list}, result: {result}')
    if result:
        return True
    else:
        return False


def check_code(mail_type: int, code: str) -> Union[UserEmail, None]:
    mail = UserEmail.objects.filter(template_id=mail_type).last()
    if mail.code == code:
        return mail
    return None


def user_forgot_password(request: Request) -> Dict:
    user_info = request.data.get('user_info')
    if not user_info:
        return {"errors": "нет данных", 'success': False}
    client = Client.objects.filter(Q(email=user_info) | Q(user__username=user_info)).first()
    if not client:
        return {"errors": "Пользователь не найден", 'success': False}
    new_password = ''.join([random.choice(string.ascii_letters) for i in range(7)])
    is_send = send_email_to_user(2, [client.email], f"user: {client.user.username}\n new_password: {new_password}\n")
    if not is_send:
        LOG.error('template dont find')
        return {"errors": "Не удалось отправить email", 'success': False}
    new_email = UserEmail(template_id=2, user=client.user)
    new_email.generate_code()
    new_email.is_view = True
    new_email.save()
    client.user.set_password(new_password)
    client.user.save()
    return {"data": {'email': client.email}, 'success': True}


def activate_user_on_email(code: str) -> Dict:
    mail = check_code(1, code)
    if mail:
        mail.user.client.activated = True
        mail.user.client.save()
        mail.is_view = True
        mail.save()
        return {'data': 'ok', 'success': True}
    else:
        return {'errors': 'Код устарел', 'success': False}


