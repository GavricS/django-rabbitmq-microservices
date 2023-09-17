from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from rest_framework import status
from django.shortcuts import render
from .serializers import OrderSerializer, ProductSerializer, OrderCreateSerializer
from decouple import config
import requests

class OrderView(APIView):
    def get(self, request, format=None):
        try:
            order_data = self.get_basic_order_data()
            invoice_data = self.get_invoices_for_orders([order_datum["id"] for order_datum in order_data])

            data = self.merge_order_invoice_data(order_data, invoice_data)

            order_serializer = OrderSerializer(data, many=True)

            render_context = {'orders': order_serializer.data}
        except Exception as exception:
            render_context = {'error': str(exception)}
        finally:
            return render(request, 'app/order/order_dashboard.html', render_context)

    def get_basic_order_data(self):
        api_url = config('GATEWAY_GET_ORDER_BASIC_INFO_ENDPOINT_URL')
        response = requests.get(api_url)

        if not response.ok:
            raise Exception('Unable to get orders at this moment.')

        return response.json()

    def get_invoices_for_orders(self, order_ids):
        api_url = config('GATEWAY_GET_INVOICES_ENDPOINT_URL')
        response = requests.post(api_url, data={'order_ids': order_ids})

        if not response.ok:
            raise Exception('Unable to get order invoices at this moment.')

        return response.json()

    def merge_order_invoice_data(self, order_data, invoice_data):
        order_data = sorted(order_data, key=lambda x: x["id"])
        invoice_data = sorted(invoice_data, key=lambda x: x["order_id"])

        invoice_data_dict = {invoice["order_id"]: invoice for invoice in invoice_data}

        for order_datum in order_data:
            order_id = order_datum["id"]

            if order_id in invoice_data_dict:
                order_datum['checkout_status'] = invoice_data_dict[order_id]['status']

                continue

            order_datum['checkout_status'] = None

        return order_data

class OrderCreateView(APIView):
    def post(self, request, format=None):
        try:
            api_url = config('GATEWAY_CREATE_ORDER_ENDPOINT_URL')

            order_create_serializer = OrderCreateSerializer(data=request.data)
            if not order_create_serializer.is_valid():
                raise Exception(order_create_serializer.errors)

            product_id = request.data.get('id')
            quantity = request.data.get('quantity')
            price = int(quantity) * int(request.data.get('price'))

            request_body = {
                "product_id": product_id,
                "quantity": quantity,
                "price": price,
            }

            response = requests.post(api_url, data=request_body)

            if not response.ok:
                raise Exception('Unable to create an order at this time.')

            return HttpResponseRedirect(redirect_to='/orders')
        except Exception as exception:
            return render(request, 'app/product/product_dashboard.html', {'error': str(exception)})

class OrderCheckoutView(APIView):
    def post(self, request, order_id, format=None):
        try:
            api_url = config('GATEWAY_CHECKOUT_ORDER_ENDPOINT_URL') + f'/{order_id}'
            response = requests.post(api_url)

            if not response.ok:
                raise Exception(f'Unable to checkout order #{order_id} at this time.')

            return HttpResponseRedirect(redirect_to='/orders')
        except Exception as exception:
            return render(request, 'app/order/order_dashboard.html', {'error': str(exception)})

class ProductView(APIView):
    def get(self, request, format=None):
        try:
            api_url = config('GATEWAY_GET_PRODUCTS_ENDPOINT_URL')
            response = requests.get(api_url)
            data = response.json()

            product_serializer = ProductSerializer(data, many=True)

            render_context = {'products': product_serializer.data}
        except Exception as exception:
            render_context = {'error': str(exception)}
        return render(request, 'app/product/product_dashboard.html', render_context)
