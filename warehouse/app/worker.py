import pika
import json
from decouple import config
import requests
import types

consts = types.SimpleNamespace()

consts.EXCHANGE_ORDER_NAME = config('EXCHANGE_ORDER_NAME')
consts.QUEUE_FINANCIAL_NAME = config('QUEUE_FINANCIAL_NAME')
consts.QUEUE_WAREHOUSE_NAME = config('QUEUE_WAREHOUSE_NAME')
consts.EXCHANGE_FINANCIAL_NAME = config('EXCHANGE_FINANCIAL_NAME')
consts.MESSAGE_TYPE_ORDER_CHECKOUT = config('MESSAGE_TYPE_ORDER_CHECKOUT')
consts.MESSAGE_TYPE_INVOICE_CONFIRM = config('MESSAGE_TYPE_INVOICE_CONFIRM')
consts.MESSAGE_TYPE_STOCK_CONFIRM = config('MESSAGE_TYPE_STOCK_CONFIRM')

def process_invoice():
    # create connection and channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config('RABBITMQ_HOST')))
    channel = connection.channel()

    # declare exchanges and queues
    channel.exchange_declare(exchange=consts.EXCHANGE_ORDER_NAME, exchange_type='direct', durable=False, auto_delete=False)
    channel.queue_declare(queue=consts.QUEUE_WAREHOUSE_NAME, durable=False, exclusive=False, auto_delete=False)
    channel.queue_bind(queue=consts.QUEUE_WAREHOUSE_NAME, exchange=consts.EXCHANGE_ORDER_NAME, routing_key='ORDER_CHECKOUT_START')
    channel.exchange_declare(exchange=consts.EXCHANGE_FINANCIAL_NAME, exchange_type='direct', durable=False, auto_delete=False)
    channel.queue_bind(queue=consts.QUEUE_WAREHOUSE_NAME, exchange=consts.EXCHANGE_FINANCIAL_NAME, routing_key='')

    print(f"[x] Warehouse worker active and awaiting messages from {consts.QUEUE_WAREHOUSE_NAME}")

    # consume messages
    try:
        channel.basic_consume(queue=consts.QUEUE_WAREHOUSE_NAME, on_message_callback=on_message_callback, auto_ack=True)
        channel.start_consuming()
    except pika.exceptions.AMQPError as exception:
        print(f"AMQP error: {exception}", flush=True)
    finally:
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
        case MESSAGE_TYPE_INVOICE_CONFIRM:
            handle_invoice_confirmation(message_body, channel)

# handle message sent on order checkout
def handle_order_checkout(message_data, channel):
    product_id = message_data['product_id']
    print(f"[.] Requesting stock availability for product #{product_id}", flush=True)
    
    message_data['in_stock'] = False
    message_data['data_type'] = consts.MESSAGE_TYPE_STOCK_CONFIRM
    
    # gets current stock for the given product and checks if it satisfies the needed order quantity
    try:
        product_stock = get_product_stock(message_data['product_id'])
        if product_stock >= message_data['quantity']:
            print("[.] Stock available", flush=True)
            message_data['in_stock'] = True
        message_data['available_stock'] = product_stock
    except Exception as exception:
        print(f"[x] Failed getting stock for product #{product_id}: ", exception, flush=True)
        return

    # publish product stock message
    channel.basic_publish(exchange='', routing_key=consts.QUEUE_FINANCIAL_NAME, body=json.dumps(message_data))
    print(f"[.] Message sent to {consts.QUEUE_FINANCIAL_NAME}", flush=True)

# handle message sent upon invoice status confirmation
def handle_invoice_confirmation(message_data, channel):
    if message_data['error']:
        return

    product_id = message_data['product_id']
    print(f"[.] Invoice updated, updating stock for product #{product_id}", flush=True)

    # decreases the stock by quantity of the product in the order
    try:
        update_stock(product_id, message_data['quantity'])
    except Exception as exception:
        print("[x] Stock update for product #{product_id} failed: ", exception, flush=True)

# gets the needed product through the warehouse API
def get_product_stock(product_id):
    response = requests.get(f'http://localhost:8000/api/v1/products/{product_id}')

    if response.status_code != requests.codes.ok:
        raise Exception(response.json())

    response = response.json()
    return response['stock']

# updates stock of the specified product through the warehouse API
def update_stock(product_id, quantity):
    data = {'quantity': -quantity}

    response = requests.put(f'http://localhost:8000/api/v1/products/stock/{product_id}', json=data)

    if response.status_code != requests.codes.ok:
        raise Exception(response.json())

process_invoice()