from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceSerializer
from rest_framework import generics
from .models import Invoice


class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

@api_view(['PUT', 'DELETE'])
def update_delete_invoice_by_order_id(request, order_id):# TODO
    return Response('success', status=status.HTTP_200_OK)