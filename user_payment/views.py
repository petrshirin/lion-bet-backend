from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from .services import make_input_request, make_output_request


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def input_request_view(request: Request) -> Response:
    response = make_input_request(request)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def output_request_view(request: Request) -> Response:
    response = make_output_request(request)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=201)
