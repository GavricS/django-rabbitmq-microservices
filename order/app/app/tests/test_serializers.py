from django.test import TestCase
from app.models import Order
from app.serializers import OrderSerializer, OrderCheckoutSerializer

class OrderSerializerTestCase(TestCase):
    def test_order_serializer_ok(self):
        order_data = {
            'id': 1,
            'product_id': 1,
            'quantity': 10,
            'price': 100
        }
        order = Order.objects.create(**order_data)

        serializer = OrderSerializer(order)

        serialized_data = serializer.data
        self.assertEqual(serialized_data, order_data)

class OrderCheckoutSerializerTestCase(TestCase):
    def test_order_checkout_serializer_create(self):
        input_data = {
            'order_id': 1,
            'product_id': 1,
            'quantity': 10,
            'price': 100
        }

        serializer = OrderCheckoutSerializer(data=input_data)
        self.assertTrue(serializer.is_valid())

        created_order = serializer.save()

        self.assertEqual(created_order.product_id, input_data['product_id'])
        self.assertEqual(created_order.quantity, input_data['quantity'])
        self.assertEqual(created_order.price, input_data['price'])

    def test_order_checkout_serializer_update(self):
        existing_order_data = {
            'id': 1,
            'product_id': 3,
            'quantity': 8,
            'price': 80
        }
        existing_order = Order.objects.create(**existing_order_data)
        updated_data = {
            'product_id': 4,
            'quantity': 12,
            'price': 120
        }

        serializer = OrderCheckoutSerializer(instance=existing_order, data=updated_data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated_order = serializer.save()

        self.assertEqual(updated_order.product_id, updated_data['product_id'])
        self.assertEqual(updated_order.quantity, updated_data['quantity'])
        self.assertEqual(updated_order.price, updated_data['price'])
