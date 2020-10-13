from .models import *
from rest_framework import serializers
from sport_events.serializers import MatchEvent, MatchWithoutEventsSerializer


class MatchEventWithMatchSerializer(serializers.ModelSerializer):

    match_list = MatchWithoutEventsSerializer(read_only=True, source='match_set', many=True)

    class Meta:
        model = MatchEvent
        fields = ('id', 'oc_group_name', 'oc_name', 'oc_rate', 'oc_pointer', 'short_name', 'match_list')


class UserBetSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserBet
        fields = ('id', 'bet_type', 'bet_code', "win_coefficient", "user_bet", "user_win", "is_went", "date_created", 'events')

    events = MatchEventWithMatchSerializer(many=True)

