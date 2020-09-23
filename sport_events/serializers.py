from rest_framework import serializers
from .models import Sport, Country, Tournament, Match, MatchEvent


class SportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sport
        fields = ('api_id', 'name', 'name_en')


class CountrySerializer(serializers.ModelSerializer):

    sport = SportSerializer()

    class Meta:
        model = Country
        fields = ('api_id', 'name', 'name_en', 'sport')


class TournamentSerializer(serializers.ModelSerializer):

    country = CountrySerializer()

    class Meta:
        model = Tournament
        fields = ('api_id', 'country', 'name', 'name_en')


class MatchEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = MatchEvent
        fields = ('id', 'oc_group_name', 'oc_name', 'oc_rate', 'oc_pointer')


class MatchSerializer(serializers.ModelSerializer):

    events = MatchEventSerializer(many=True)
    tournament = TournamentSerializer()

    class Meta:
        model = Match
        fields = ('game_num', 'name', 'name_en', 'game_start',
                  'opp_1_name', 'opp_2_name', 'opp_1_id', 'opp_2_id', 'opp_1_icon', 'opp_2_icon',
                  'tournament', 'score_full', 'score_period', 'period_name', 'events')

