from rest_framework import serializers
from .models import ClientRequest, Department


class ClientRequestSerializer(serializers.ModelSerializer):

    department = serializers.CharField(source='department.name')

    class Meta:
        model = ClientRequest
        fields = ('number', 'department', 'request', 'email_to_answer', 'closed')


class ClientRequestPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientRequest
        fields = ('department', 'request', 'email_to_answer')


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('id', 'name')

