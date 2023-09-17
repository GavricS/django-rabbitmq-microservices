from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Invoice.StatusChoices.choices)

class OrderIdsSerializer(serializers.Serializer):
    order_ids = serializers.ListField(child=serializers.IntegerField())