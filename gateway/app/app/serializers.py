from rest_framework import serializers

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    checkout_status = serializers.CharField()

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    stock = serializers.IntegerField()
    price = serializers.IntegerField()
