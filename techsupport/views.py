from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from .services import get_client_requests, get_all_departments, \
    process_user_request_to_tech_support, send_mail_from_contacts


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def opened_tech_request_view(request: Request) -> Response:
    requests = get_client_requests(request)
    return Response({'data': requests, 'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tech_support_department_view(request: Request):
    departments = get_all_departments()
    return Response({'data': departments, 'success': True})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_new_request_view(request: Request):
    new_request = process_user_request_to_tech_support(request)
    if new_request.get('errors'):
        return Response(new_request, status=422)
    else:
        return Response(new_request, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def feedback_view(request: Request) -> Response:
    if request.data.get('name') and request.data.get('phone') and request.data.get('text'):
        response = send_mail_from_contacts(request.data.get('name'),
                                           request.data.get('phone'),
                                           request.data.get('text'))
        if response.get('errors'):
            return Response(response, status=400)
        return Response(response, status=201)
    return Response({"success": False, 'errors': "Неверные параметры"})




