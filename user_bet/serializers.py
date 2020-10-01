from .models import *
from rest_framework import serializers
from sport_events.serializers import MatchEventSerializer


class UserBetSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserBet
        fields = ('id', 'bet_type', 'bet_code', "win_coefficient", "user_bet", "user_win", "is_went", "date_created", 'events')

    events = MatchEventSerializer(many=True)

