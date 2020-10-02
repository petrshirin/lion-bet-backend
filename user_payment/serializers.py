from rest_framework import serializers
from .models import UserMoneyRequest


class UserMoneyRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMoneyRequest
        fields = ('user_id', 'request_type', 'amount', 'date_created', 'accepted')


