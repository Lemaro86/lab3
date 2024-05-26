from rest_framework import serializers
from stocks.models import *
from collections import OrderedDict


class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_staff', 'is_superuser']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["pk", "title", "description", "url", "cost"]

    def get_fields(self):
        new_fields = OrderedDict()
        for name, field in super().get_fields().items():
            field.required = False
            new_fields[name] = field
        return new_fields


class ServiceShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["pk"]


class OrderSerializer(serializers.ModelSerializer):
    service = ServiceShortSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ["pk", "status", "created", "activated", "completed", "creator_id",  "moderator_id", "service"]


class UserRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["is_staff", "is_superuser"]
