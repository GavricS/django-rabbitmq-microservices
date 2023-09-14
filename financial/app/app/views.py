from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceSerializer, InvoiceStatusSerializer, OrderIdsSerializer
from rest_framework import generics
from .models import Invoice
from rest_framework.views import APIView


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class UpdateDeleteInvoiceByOrderIdView(APIView):
    def put(self, request, order_id, format=None):
        try:
            product = Invoice.objects.get(order_id=order_id)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = InvoiceStatusSerializer(product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id, format=None):
        try:
            product = Invoice.objects.get(order_id=order_id)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class GetInvoicesByOrderIdView(APIView):
    def post(self, request, format=None):
        serializer = OrderIdsSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        order_ids = serializer.validated_data['order_ids']

        invoices = Invoice.objects.filter(order_id__in=order_ids)

        serializer = InvoiceSerializer(invoices, many=True)

        return Response(serializer.data)
