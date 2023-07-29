import pika
import json
import requests
from decouple import config
from rest_framework import status
import types

consts = types.SimpleNamespace()

consts.EXCHANGE_ORDER_NAME = config('EXCHANGE_ORDER_NAME')
consts.QUEUE_FINANCIAL_NAME = config('QUEUE_FINANCIAL_NAME')
consts.EXCHANGE_FINANCIAL_NAME = config('EXCHANGE_FINANCIAL_NAME')
consts.MESSAGE_TYPE_ORDER_CHECKOUT = config('MESSAGE_TYPE_ORDER_CHECKOUT')
consts.MESSAGE_TYPE_STOCK_CONFIRM = config('MESSAGE_TYPE_STOCK_CONFIRM')
consts.MESSAGE_TYPE_INVOICE_CONFIRM = config('MESSAGE_TYPE_INVOICE_CONFIRM')

def process_invoice():
    # create connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config('RABBITMQ_HOST')))
    channel = connection.channel()

    # declare exchanges and queues
    channel.exchange_declare(exchange=consts.EXCHANGE_ORDER_NAME, exchange_type='direct', durable=False, auto_delete=False)
    channel.queue_declare(queue=consts.QUEUE_FINANCIAL_NAME, durable=False, auto_delete=False)
    channel.exchange_declare(exchange=consts.EXCHANGE_FINANCIAL_NAME, exchange_type='direct', durable=False, auto_delete=False)
    channel.queue_bind(queue=consts.QUEUE_FINANCIAL_NAME, exchange=consts.EXCHANGE_ORDER_NAME, routing_key='')

    print(f"[x] Financial worker active and awaiting messages from {consts.QUEUE_FINANCIAL_NAME}", flush=True)

    # consume messages
    try:
        channel.basic_consume(queue=consts.QUEUE_FINANCIAL_NAME, on_message_callback=on_message_callback, auto_ack=True)
        channel.start_consuming()
    except pika.exceptions.AMQPError as exception:
            print(f"AMQP error: {exception}", flush=True)
    finally:
        # free resources
        channel.close()
        connection.close()

# function called when message received
def on_message_callback(channel, method, properties, body):
    message_body = json.loads(body)
    message_type = message_body['data_type']

    # handle specific message types
    match message_type:
        case consts.MESSAGE_TYPE_ORDER_CHECKOUT:
            handle_order_checkout(message_body, channel)
        case consts.MESSAGE_TYPE_STOCK_CONFIRM:
            handle_stock_confirmation(message_body, channel)

# handle message sent on order checkout
def handle_order_checkout(message_data, channel):
    order_id = message_data['order_id']
    print(f"[.] Creating invoice for order #{order_id}", flush=True)

    data = {
        'order_id': order_id,
        'total': message_data['price'],
        'status': 'incomplete'
    }

    # creates an invoice for the given order
    try:
        create_invoice(data)
    except Exception as exception:
        print('[x] Invoice creation failed: ', exception, flush=True)
        return
    
    print(f"[.] Successfully created an invoice for order #{order_id}", flush=True)

# handle message sent upon product stock confirmation
def handle_stock_confirmation(message_data, channel):
    order_id = message_data['order_id']

    message_data['invoice_confirmed'] = False
    message_data['error'] = None
    message_data['data_type'] = consts.MESSAGE_TYPE_INVOICE_CONFIRM

    # if there is not enough stock for the given order, the previously created invoice should be deleted
    if not message_data['in_stock']:
        print("[x] Insufficient stock - deleting invoice", flush=True)
        try:
            delete_invoice(order_id)
        except Exception as exception:
            print(f"[x] Invoice deletion for order #{order_id} failed: ", exception, flush=True)
    # if there is enough stock for the given order, the status of the order invoice should be updated
    else:
        print(f"[.] Stock confirmed, updating invoice for order #{order_id}", flush=True)
        data = {'status': 'waiting'}
        try:
            update_invoice(order_id, data)
            message_data['invoice_confirmed'] = True
        except Exception as exception:
            print(f"[x] Invoice update for order #{order_id} failed: ", exception, flush=True)

    message = json.dumps(message_data)
    channel.basic_publish(exchange=consts.EXCHANGE_FINANCIAL_NAME, routing_key='', body=message)
    print(f"[.] Message sent to {consts.EXCHANGE_FINANCIAL_NAME}", flush=True)

# creates an invoice for the given order through the financial API
def create_invoice(data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://localhost:8000/api/v1/invoices', json=data, headers=headers)
    
    if response.status_code != requests.codes.created:
        raise Exception(response.json())

# updates status of the given order's invoice through the financial API
def update_invoice(order_id, data):
    url = f'http://localhost:8000/api/v1/invoices/orders/{order_id}'
    headers = {'Content-Type': 'application/json'}

    response = requests.put(url, json=data, headers=headers)

    if response.status_code != requests.codes.ok:
        raise Exception(response.json())

# deletes the given order's invoice through the financial API
def delete_invoice(order_id):
    url = f'http://localhost:8000/api/v1/invoices/orders/{order_id}'

    response = requests.delete(url)

    if response.status_code != requests.codes.no_content:
        raise Exception(response.json())

process_invoice()