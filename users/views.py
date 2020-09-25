from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from .services import get_self_info_client, register_client, change_password, change_client_info, user_forgot_password, activate_user_on_email


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_view(request: Request) -> Response:
    data = get_self_info_client(request)
    return Response({'data': data, 'success': True}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_client_view(request: Request) -> Response:
    response = register_client(request)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_user_password_view(request: Request) -> Response:
    res = change_password(request)
    if res.get('errors'):
        return Response(res, status=400)
    else:
        return Response(res, status=200)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_client_info_view(request: Request) -> Response:

    res = change_client_info(request)
    if res.get('errors'):
        return Response(res, status=422)
    else:
        return Response(res, status=202)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password_view(request: Request) -> Response:

    res = user_forgot_password(request)
    if res.get('errors'):
        return Response(res, status=422)
    else:
        return Response(res, status=202)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_user_for_email_view(request: Request, code: str) -> Response:
    """
    Activate account when client navigates to email url
    :param code: unique code in url
    :param request:
    :return:
    """
    response = activate_user_on_email(code)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=200)



