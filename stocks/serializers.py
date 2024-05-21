from rest_framework import serializers
from stocks.models import Service
from stocks.models import Order
from collections import OrderedDict
from stocks.models import CustomUser


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


class OrderSerializer(serializers.ModelSerializer):
    # service_set = ServiceSerializer(read_only=True)
    # status: created, activated, completed, declined

    class Meta:
        model = Order
        fields = ["order_id", "status", "created", "activated", "completed", "creator_id",  "moderator_id"]
