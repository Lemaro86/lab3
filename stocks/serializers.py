from stocks.models import AuthUser
from rest_framework import serializers
from stocks.models import Service
from stocks.models import Order


class UserSerializer(serializers.ModelSerializer):
    # stock_set = StockSerializer(many=True, read_only=True)

    class Meta:
        model = AuthUser
        fields = ["id", "first_name", "last_name"]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["pk", "title", "description", "url", "cost"]


class OrderSerializer(serializers.ModelSerializer):
    # service_set = ServiceSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["order_id", "status", "created", "activated", "completed", "creator_id",  "moderator_id"]
