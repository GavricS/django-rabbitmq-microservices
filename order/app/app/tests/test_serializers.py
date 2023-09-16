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
    def test_order_checkout_serializer_create_ok(self):
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

    def test_order_checkout_serializer_create_missing_order_id_fail(self):
        input_data = {
            'product_id': 1,
            'quantity': 10,
            'price': 100
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('order_id', serializer.errors)

    def test_order_checkout_serializer_create_missing_product_id_fail(self):
        input_data = {
            'order_id': 1,
            'quantity': 10,
            'price': 100
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)

    def test_order_checkout_serializer_create_missing_quantity_fail(self):
        input_data = {
            'order_id': 1,
            'product_id': 1,
            'price': 100
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_checkout_serializer_create_missing_price_fail(self):
        input_data = {
            'order_id': 1,
            'product_id': 1,
            'quantity': 10,
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_checkout_serializer_create_non_integer_order_id_fail(self):
        input_data = {
            'order_id': 'test',
            'product_id': 1,
            'quantity': 10,
            'price': 100
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('order_id', serializer.errors)

    def test_order_checkout_serializer_create_non_integer_product_id_fail(self):
        input_data = {
            'order_id': 1,
            'product_id': 'test',
            'quantity': 10,
            'price': 100
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)

    def test_order_checkout_serializer_create_non_integer_quantity_fail(self):
        input_data = {
            'order_id': 1,
            'product_id': 1,
            'quantity': 'test',
            'price': 100
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_checkout_serializer_create_non_integer_price_fail(self):
        input_data = {
            'order_id': 1,
            'product_id': 1,
            'quantity': 10,
            'price': 'test',
        }

        serializer = OrderCheckoutSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_checkout_serializer_update_ok(self):
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

    def test_order_checkout_serializer_update_non_integer_product_id_fail(self):
        existing_order_data = {
            'id': 1,
            'product_id': 3,
            'quantity': 8,
            'price': 80
        }
        existing_order = Order.objects.create(**existing_order_data)
        updated_data = {
            'product_id': 'test',
            'quantity': 12,
            'price': 120
        }

        serializer = OrderCheckoutSerializer(instance=existing_order, data=updated_data, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)

    def test_order_checkout_serializer_update_non_integer_quantity_fail(self):
        existing_order_data = {
            'id': 1,
            'product_id': 3,
            'quantity': 8,
            'price': 80
        }
        existing_order = Order.objects.create(**existing_order_data)
        updated_data = {
            'product_id': 4,
            'quantity': 'test',
            'price': 120
        }

        serializer = OrderCheckoutSerializer(instance=existing_order, data=updated_data, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_checkout_serializer_update_non_integer_price_fail(self):
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
            'price': 'test'
        }

        serializer = OrderCheckoutSerializer(instance=existing_order, data=updated_data, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_checkout_serializer_update_missing_product_ok(self):
        existing_order_data = {
            'id': 1,
            'product_id': 3,
            'quantity': 8,
            'price': 80
        }
        existing_order = Order.objects.create(**existing_order_data)
        updated_data = {
            'quantity': 12,
            'price': 120
        }

        serializer = OrderCheckoutSerializer(instance=existing_order, data=updated_data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated_order = serializer.save()

        self.assertEqual(updated_order.quantity, updated_data['quantity'])
        self.assertEqual(updated_order.price, updated_data['price'])

    def test_order_checkout_serializer_update_missing_quantity_ok(self):
        existing_order_data = {
            'id': 1,
            'product_id': 3,
            'quantity': 8,
            'price': 80
        }
        existing_order = Order.objects.create(**existing_order_data)
        updated_data = {
            'product_id': 4,
            'price': 120
        }

        serializer = OrderCheckoutSerializer(instance=existing_order, data=updated_data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated_order = serializer.save()

        self.assertEqual(updated_order.product_id, updated_data['product_id'])
        self.assertEqual(updated_order.price, updated_data['price'])

    def test_order_checkout_serializer_update_missing_price_ok(self):
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
        }

        serializer = OrderCheckoutSerializer(instance=existing_order, data=updated_data, partial=True)

        self.assertTrue(serializer.is_valid())

        updated_order = serializer.save()

        self.assertEqual(updated_order.product_id, updated_data['product_id'])
        self.assertEqual(updated_order.quantity, updated_data['quantity'])
