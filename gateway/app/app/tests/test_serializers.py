from django.test import TestCase
from app.serializers import OrderSerializer, OrderCreateSerializer, ProductSerializer
from rest_framework import serializers

class OrderSerializerTestCase(TestCase):
    def test_order_serializer_ok(self):
        data = {
            'id': 1,
            'product_id': 2,
            'quantity': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_order_serializer_missing_id_fail(self):
        data = {
            'product_id': 2,
            'quantity': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_order_serializer_missing_product_id_fail(self):
        data = {
            'id': 1,
            'quantity': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)

    def test_order_serializer_missing_quantity_fail(self):
        data = {
            'id': 1,
            'product_id': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_serializer_missing_price_fail(self):
        data = {
            'id': 1,
            'product_id': 10,
            'quantity': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_serializer_missing_checkout_status_fail(self):
        data = {
            'id': 1,
            'product_id': 10,
            'quantity': 100,
            'price': 100,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('checkout_status', serializer.errors)

    def test_order_serializer_non_integer_id_fail(self):
        data = {
            'id': 'test',
            'product_id': 2,
            'quantity': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_order_serializer_non_integer_product_id_fail(self):
        data = {
            'id': 1,
            'product_id': 'test',
            'quantity': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)

    def test_order_serializer_non_integer_quantity_fail(self):
        data = {
            'id': 1,
            'product_id': 2,
            'quantity': 'test',
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_serializer_non_integer_price_fail(self):
        data = {
            'id': 1,
            'product_id': 2,
            'quantity': 10,
            'price': 'test',
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_serializer_missing_checkout_status_fail(self):
        data = {
            'id': 1,
            'product_id': 2,
            'quantity': 10,
            'price': 100,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('checkout_status', serializer.errors)

    def test_order_serializer_negative_id_fail(self):
        data = {
            'id': -1,
            'product_id': 2,
            'quantity': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_order_serializer_negative_product_id_fail(self):
        data = {
            'id': 1,
            'product_id': -2,
            'quantity': 10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('product_id', serializer.errors)

    def test_order_serializer_negative_quantity_fail(self):
        data = {
            'id': 1,
            'product_id': 2,
            'quantity': -10,
            'price': 100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_serializer_negative_price_fail(self):
        data = {
            'id': 1,
            'product_id': 2,
            'quantity': 10,
            'price': -100,
            'checkout_status': 'complete',
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_serializer_non_char_checkout_status_fail(self):
        data = {
            'id': 1,
            'product_id': 2,
            'quantity': 10,
            'price': 100,
            'checkout_status': None,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('checkout_status', serializer.errors)

class OrderCreateSerializerTestCase(TestCase):
    def test_order_create_serializer_ok(self):
        data = {
            'id': 1,
            'quantity': 10,
            'price': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_order_create_serializer_missing_id_fail(self):
        data = {
            'quantity': 10,
            'price': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_order_create_serializer_missing_quantity_fail(self):
        data = {
            'id': 1,
            'price': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_create_serializer_missing_price_fail(self):
        data = {
            'id': 1,
            'quantity': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_create_serializer_non_integer_id_fail(self):
        data = {
            'id': 'test',
            'quantity': 10,
            'price': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_order_create_serializer_non_integer_quantity_fail(self):
        data = {
            'id': 1,
            'quantity': 'test',
            'price': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_create_serializer_non_integer_price_fail(self):
        data = {
            'id': 1,
            'quantity': 10,
            'price': 'test',
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_order_create_serializer_negative_id_fail(self):
        data = {
            'id': -1,
            'quantity': 10,
            'price': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_order_create_serializer_negative_quantity_fail(self):
        data = {
            'id': 1,
            'quantity': -10,
            'price': 100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_order_create_serializer_negative_price_fail(self):
        data = {
            'id': 1,
            'quantity': 10,
            'price': -100,
        }

        serializer = OrderCreateSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

class ProductSerializerTestCase(TestCase):
    def test_product_serializer_ok(self):
        data = {
            'id': 1,
            'stock': 100,
            'price': 50,
        }

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_product_serializer_missing_id_fail(self):
        data = {
            'stock': 100,
            'price': 50,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_product_serializer_missing_stock_fail(self):
        data = {
            'id': 1,
            'price': 50,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('stock', serializer.errors)

    def test_product_serializer_missing_price_fail(self):
        data = {
            'id': 1,
            'stock': 100,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_product_serializer_non_integer_id_fail(self):
        data = {
            'id': 'test',
            'stock': 100,
            'price': 50,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_product_serializer_non_integer_stock_fail(self):
        data = {
            'id': 1,
            'stock': 'test',
            'price': 50,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('stock', serializer.errors)

    def test_product_serializer_non_integer_price_fail(self):
        data = {
            'id': 1,
            'stock': 100,
            'price': 'test',
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)

    def test_product_serializer_non_integer_id_fail(self):
        data = {
            'id': -1,
            'stock': 100,
            'price': 50,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('id', serializer.errors)

    def test_product_serializer_non_integer_stock_fail(self):
        data = {
            'id': 1,
            'stock': -100,
            'price': 50,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('stock', serializer.errors)

    def test_product_serializer_non_integer_price_fail(self):
        data = {
            'id': 1,
            'stock': 100,
            'price': -50,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
