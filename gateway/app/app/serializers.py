from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    product_id = serializers.IntegerField(min_value=0)
    quantity = serializers.IntegerField(min_value=0)
    price = serializers.IntegerField(min_value=0)
    checkout_status = serializers.CharField()

class OrderCreateSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    quantity = serializers.IntegerField(min_value=0)
    price = serializers.IntegerField(min_value=0)

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    stock = serializers.IntegerField(min_value=0)
    price = serializers.IntegerField(min_value=0)
