from .models import *
from rest_framework.request import Request
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict
from .serializers import ClientRequestSerializer, ClientRequestPostSerializer, DepartmentSerializer
from rest_framework.serializers import ModelSerializer
from typing import Optional, List, \
    Dict, Any, Union


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


def validate_and_write_request_to_db(request: Request) -> ModelSerializer:
    ser = ClientRequestPostSerializer(data=request.data)
    if ser.is_valid():
        ClientRequest.objects.create(user=request.user, **ser.validated_data)
        return ser
    else:
        return ser


