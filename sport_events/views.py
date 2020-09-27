from django.shortcuts import render
from rest_framework.views import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from .services.line_events import get_line_sports, get_line_countries, get_line_tournaments, get_line_matches, get_list_of_tournaments_with_matches_line
from .services.live_events import get_live_sports, get_live_countries, get_live_tournaments, get_live_matches, get_list_of_tournaments_with_matches_live


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sports_line_view(request: Request) -> Response:

    sports = get_line_sports()

    return Response({'success': True, 'data': sports}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def country_line_view(request: Request, sport_id: int = None) -> Response:
    countries = get_line_countries(sport_id)

    return Response({'success': True, 'data': countries}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournaments_line_view(request: Request, sport_id: int = None, country_id: int = None, count: int = None) -> Response:

    tournaments = get_line_tournaments(sport_id, country_id, count)

    return Response({'success': True, 'data': tournaments}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matches_line_view(request: Request, tournament_id: int = None, count: int = None) -> Response:

    matches = get_line_matches(tournament_id, count)

    return Response({'success': True, 'data': matches}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sports_live_view(request: Request) -> Response:

    sports = get_live_sports()

    return Response({'success': True, 'data': sports}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def country_live_view(request: Request, sport_id: int = None) -> Response:
    countries = get_live_countries(sport_id)

    return Response({'success': True, 'data': countries}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournaments_live_view(request: Request, sport_id: int = None, country_id: int = None, count: int = None) -> Response:

    tournaments = get_live_tournaments(sport_id, country_id, count)

    return Response({'success': True, 'data': tournaments}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def matches_live_view(request: Request, tournament_id: int = None, count: int = None) -> Response:

    matches = get_live_matches(tournament_id, count)

    return Response({'success': True, 'data': matches}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournaments_with_matches_line_view(request: Request, sport_id: int = 0) -> Response:

    tournaments_data = get_list_of_tournaments_with_matches_line(sport_id)

    return Response({'success': True, 'data': tournaments_data}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tournaments_with_matches_live_view(request: Request, sport_id: int = 0) -> Response:

    tournaments_data = get_list_of_tournaments_with_matches_live(sport_id)

    return Response({'success': True, 'data': tournaments_data}, status=200)

