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
        print("DEBUG in order checkout endpoint", flush=True)
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
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=config('RABBITMQ_HOST')))#TODO make sure there is no potential deadlock - inspect the BlockingConnection class for more info
        channel = connection.channel()

        # declare exchanges and queue
        channel.exchange_declare(exchange=EXCHANGE_ORDER_NAME, exchange_type='direct', durable=False, auto_delete=False)
        channel.queue_declare(queue=QUEUE_ORDER_NAME, durable=False, auto_delete=False)
        channel.exchange_declare(exchange=EXCHANGE_FINANCIAL_NAME, exchange_type='direct', durable=False, auto_delete=False)
        channel.queue_bind(queue=QUEUE_ORDER_NAME, exchange=EXCHANGE_FINANCIAL_NAME, routing_key='')

        # serialize message
        message = json.dumps(serialized_order_data)

        # publish order checkout message
        channel.basic_publish(exchange=EXCHANGE_ORDER_NAME, routing_key='', body=message)

        result = None
        # define on message callback
        def on_message_callback(channel, method, properties, body):
            nonlocal result#, request_processed
            # TODO maybe additional message confirmation logic needed?
            print("[.] Checkout successful", flush=True)
            message_body = json.loads(body)
            print("DEBUG order: response body: ", body, flush=True)
            result = message_body

        # wait for response (blocking)
        channel.basic_consume(queue=QUEUE_ORDER_NAME, on_message_callback=on_message_callback, auto_ack=True)

        try:
            channel.connection.process_data_events(time_limit=20)
        except pika.exceptions.AMQPError as exception:
            print(f"AMQP error: {exception}")# TODO error handling

        # free resources
        channel.close()
        connection.close()

        # return response
        return Response(result, status=status.HTTP_200_OK)