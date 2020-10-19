from .models import *
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from .serializers import ClientRequestSerializer, ClientRequestPostSerializer, DepartmentSerializer
from rest_framework.serializers import ModelSerializer
from typing import Optional, List, \
    Dict, Any, Union
from users.models import UserEmail, EmailTemplate
from django.core.mail import send_mail
import logging
from smtplib import SMTPException

LOG = logging.getLogger(__name__)


def process_user_request_to_tech_support(request: Request):
    """
    This func create new client request for tech support
    :param request:
    :return:
    """
    res = validate_and_write_request_to_db(request)
    if res.errors:
        return {'errors': res.errors, 'success': False}
    else:
        return {'data': res.data, 'success': True}


def get_client_requests(request: Request) -> ReturnList:
    """
    Get all opened user requests and return it
    :param request:
    :return:
    """
    requests = ClientRequest.objects.filter(user=request.user, closed=False).all()
    ser = ClientRequestSerializer(requests, many=True)
    return ser.data


def get_all_departments() -> ReturnList:
    """
    Get all departments of Tech Support in DB and return it
    :return:
    """
    departments = Department.objects.all()
    ser = DepartmentSerializer(departments, many=True)
    return ser.data


def send_mail_from_contacts(name: str, phone: str, text: str) -> Dict:
    is_send = _send_letter_to_info_email({'name': name,
                                          'phone': phone,
                                          'text': text})
    if is_send:
        return {"success": True, 'data': 'ok'}
    return {'success': False, 'errors': "Не удалось отправить письмо"}


def validate_and_write_request_to_db(request: Request) -> ModelSerializer:
    ser = ClientRequestPostSerializer(data=request.data)
    if ser.is_valid():
        ClientRequest.objects.create(user=request.user, **ser.validated_data)
        return ser
    else:
        return ser


def _send_letter_to_info_email(data_info: Dict, email_to_send: str = 'info@royal-lion.bet') -> bool:
    try:
        template = EmailTemplate.objects.get(pk=3)
    except EmailTemplate.DoesNotExist:
        return False
    try:
        send_mail(template.subject, template.text.format(data_info.get('name'),
                                                         data_info.get('phone'),
                                                         data_info.get('text')), template.from_email, [email_to_send])
    except SMTPException as e:
        LOG.error(e)
        return False
    LOG.info(f'Email of type 3 send on')
    return True
