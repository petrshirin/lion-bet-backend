
from rest_framework import serializers
from .models import Client, Gender, User


class ClientInfoSerializer(serializers.ModelSerializer):

    gender = serializers.CharField(source='gender.name')

    class Meta:
        model = Client
        fields = ('id', 'first_name', 'second_name', 'email',
                  'date_birth', 'phone_number', 'gender', 'city')


class ClientRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('first_name', 'second_name', 'email',
                  'date_birth', 'phone_number', 'gender', 'city')


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=32, min_length=4)
    password1 = serializers.CharField(max_length=32, min_length=4)
    password2 = serializers.CharField(max_length=32, min_length=4)


class ChangeClientInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('phone_number', 'email')
