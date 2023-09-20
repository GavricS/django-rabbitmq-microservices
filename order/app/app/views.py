import json
from django.shortcuts import render
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .serializers import OrderSerializer, OrderCheckoutSerializer
from rest_framework import generics
from .models import Order
from decouple import config
import pika

QUEUE_ORDER_NAME = config('QUEUE_ORDER_NAME')
EXCHANGE_ORDER_NAME = config('EXCHANGE_ORDER_NAME')
EXCHANGE_FINANCIAL_NAME = config('EXCHANGE_FINANCIAL_NAME')
MESSAGE_TYPE_ORDER_CHECKOUT = config('MESSAGE_TYPE_ORDER_CHECKOUT')

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderCheckoutView(APIView):
    def post(self, request, pk, format=None):
        # find order
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=404)
        
        # serialize order data
        order_serializer = OrderCheckoutSerializer(order)
        serialized_order_data = order_serializer.data
        serialized_order_data['data_type'] = MESSAGE_TYPE_ORDER_CHECKOUT

        # create connection and channel
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config('RABBITMQ_HOST')))
        channel = connection.channel()

        # declare exchanges and queue
        channel.exchange_declare(exchange=EXCHANGE_ORDER_NAME, exchange_type='direct', durable=False, auto_delete=False)
        channel.queue_declare(queue=QUEUE_ORDER_NAME, durable=False, auto_delete=False)
        channel.exchange_declare(exchange=EXCHANGE_FINANCIAL_NAME, exchange_type='direct', durable=False, auto_delete=False)
        channel.queue_bind(queue=QUEUE_ORDER_NAME, exchange=EXCHANGE_FINANCIAL_NAME, routing_key='ORDER_CHECKOUT_PROCESSED')

        # serialize message
        message = json.dumps(serialized_order_data)

        # publish order checkout message
        channel.basic_publish(exchange=EXCHANGE_ORDER_NAME, routing_key='ORDER_CHECKOUT_START', body=message)

        result = None
        # define on message callback
        def on_message_callback(channel, method, properties, body):
            nonlocal result
            message_body = json.loads(body)

            result = None if not message_body["error"] else {'error': message_body["error"]}

        # wait for response (blocking)
        channel.basic_consume(queue=QUEUE_ORDER_NAME, on_message_callback=on_message_callback, auto_ack=True)

        try:
            channel.connection.process_data_events(time_limit=config('ORDER_CHECKOUT_ENDPOINT_TIME_LIMIT', cast=int))
        except pika.exceptions.AMQPError as exception:
            print(f"AMQP error: {exception}")

        # free resources
        channel.close()
        connection.close()

        # return response
        response_status = status.HTTP_204_NO_CONTENT if not result else status.HTTP_500_INTERNAL_SERVER_ERROR
        return Response(result, response_status)