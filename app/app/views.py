from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .serializers import OrderSerializer
from rest_framework import generics
from .models import Order
import pika

QUEUE_ORDER_NAME = 'OrderQueue'
EXCHANGE_ORDER_NAME = 'OrderExchange'
EXCHANGE_FINANCIAL_NAME = 'FinancialExchange'

# @api_view(['POST'])
# def create_order(request):
#     serializer = OrderSerializer(data=request.data)# TODO exception handling

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(['GET'])
def order_checkout(request, id):# this should be refactored
    try:
        order = Order.objects.get(pk=id)
    except Order.DoesNotExist:# TODO exception handling
        return Response(status=404)
    
    serializer = OrderSerializer(order)
    serialized_order_data = Response(serializer.data)

    order_queue_name = QUEUE_ORDER_NAME# extract into env var
    order_exchange_name = EXCHANGE_ORDER_NAME
    financial_exchange_name = EXCHANGE_FINANCIAL_NAME
    request_processed = False
    res = None

    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))# TODO make sure there is no potential deadlock - inspect the BlockingConnection class for more info
    channel = connection.channel()

    # Declare exchanges and queues
    channel.exchange_declare(exchange=order_exchange_name, exchange_type='direct', durable=False, auto_delete=False)
    channel.queue_declare(queue=order_queue_name, durable=False, auto_delete=False)
    channel.exchange_declare(exchange=financial_exchange_name, exchange_type='direct', durable=False, auto_delete=False)
    channel.queue_bind(queue=order_queue_name, exchange=financial_exchange_name)

    # Prepare message
    message = str(serialized_order_data)

    # Send message to exchange
    channel.basic_publish(exchange=order_exchange_name, routing_key='', body=message)

    # Callback function for receiving messages
    def on_message(channel, method, properties, body):
        nonlocal res, request_processed
        res = body
        request_processed = True

    # Receive message
    channel.basic_consume(queue=order_queue_name, on_message_callback=on_message, auto_ack=True)

    # Wait for only 1 message with a timeout of 30 seconds
    while request_processed != True:
        try:
            channel.connection.process_data_events(time_limit=30)
        except KeyboardInterrupt:
            break
        except pika.exceptions.AMQPError as e:
            print(f"AMQP Error: {e}")
            break

    # Close connection and channel
    channel.close()
    connection.close()

    # Return result
    return res
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)