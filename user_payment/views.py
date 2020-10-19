from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from .services import make_input_request, make_output_request, user_output_requests, user_input_requests


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_input_request_view(request: Request) -> Response:
    response = make_input_request(request)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_output_request_view(request: Request) -> Response:
    response = make_output_request(request)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_output_request_view(request: Request) -> Response:
    response = user_output_requests(request.user)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_input_request_view(request: Request) -> Response:
    response = user_input_requests(request.user)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=200)

