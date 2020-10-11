from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from .services.make_bet import make_bet
from .services.find_bet import get_users_bet, get_bet_on_ticket
from .services.process_bet import process_bet_status
import logging


LOG = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([AllowAny])
def make_bet_view(request: Request, bet_type: str) -> Response:

    if bet_type != "live" and bet_type != "line":
        return Response({"errors": "Невалидный тип ставки", "success": False}, status=422)
    response = make_bet(request, bet_type)
    if response.get('errors'):
        return Response(response, status=400)
    return Response(response, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_bet_for_ticket_view(request: Request, ticket: str) -> Response:
    response = get_bet_on_ticket(request.user, ticket)
    if response.get('errors'):
        return Response(response, status=400)
    else:
        return Response(response, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_user_bet_view(request: Request) -> Response:
    response = get_users_bet(request.user)
    return Response(response, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def process_bet_view(request: Request) -> Response:
    is_processed = process_bet_status(request)
    if not is_processed:
        LOG.error(f"Error in process bet {request.data}")
    return Response('ok', status=200)
