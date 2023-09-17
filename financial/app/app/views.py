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
            invoice = Invoice.objects.get(order_id=order_id)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)

        extra_fields = set(request.data.keys()) - {'status'}
        if extra_fields:
            return Response(
                {"error": f"Unexpected fields: {', '.join(extra_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = InvoiceStatusSerializer(data=request.data)
        if serializer.is_valid():
            invoice.status = serializer.validated_data['status']
            invoice.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id, format=None):
        try:
            invoice = Invoice.objects.get(order_id=order_id)
        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)
        
        invoice.delete()
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
