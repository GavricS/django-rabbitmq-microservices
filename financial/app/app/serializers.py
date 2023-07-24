from rest_framework import serializers
from .models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['status']

    def validate(self, data):#TODO validate value?
        if 'status' not in data:
            raise serializers.ValidationError("The 'status' field is required.")
        return data