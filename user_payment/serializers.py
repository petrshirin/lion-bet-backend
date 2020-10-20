from rest_framework import serializers
from .models import UserMoneyRequest


class UserMoneyRequestSerializer(serializers.ModelSerializer):

    account_number = serializers.CharField(source='get_hidden_account_number')

    class Meta:
        model = UserMoneyRequest
        fields = ('user_id', 'request_type', 'amount', 'date_created', 'accepted', 'request_type', 'account_number')


