from django.test import TestCase
from app.models import Invoice
from app.serializers import InvoiceSerializer, InvoiceStatusSerializer, OrderIdsSerializer

class InvoiceSerializerTestCase(TestCase):
    def test_invoice_serializer_ok(self):
        invoice_data = {
            'id': 1,
            'order_id': 1,
            'total': 10,
            'status': Invoice.StatusChoices.WAITING
        }
        invoice = Invoice.objects.create(**invoice_data)

        serializer = InvoiceSerializer(invoice)

        serialized_data = serializer.data
        self.assertEqual(serialized_data, invoice_data)

class InvoiceStatusSerializerTestCase(TestCase):
    def test_invoice_status_serializer_ok(self):
        input_data = {
            'status': Invoice.StatusChoices.WAITING
        }

        serializer = InvoiceStatusSerializer(data=input_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, input_data)

    def test_invoice_status_serializer_missing_status_fail(self):
        input_data = {}

        serializer = InvoiceStatusSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_invoice_status_serializer_non_string_status_fail(self):
        input_data = {
            'status': 1
        }

        serializer = InvoiceStatusSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

    def test_invoice_status_serializer_invalid_string_value_status_fail(self):
        input_data = {
            'status': 'test'
        }

        serializer = InvoiceStatusSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)

class OrderIdsSerializerTestCase(TestCase):
    def test_invoice_order_ids_serializer_ok(self):
        input_data = {
            'order_ids': [1, 2, 3]
        }

        serializer = OrderIdsSerializer(data=input_data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data, input_data)

    def test_invoice_order_ids_serializer_missing_order_ids_fail(self):
        input_data = {}

        serializer = OrderIdsSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('order_ids', serializer.errors)

    def test_invoice_order_ids_serializer_non_array_order_ids_fail(self):
        input_data = {
            'order_ids': 1
        }

        serializer = OrderIdsSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('order_ids', serializer.errors)

    def test_invoice_order_ids_serializer_non_integer_order_ids_fail(self):
        input_data = {
            'order_ids': [1, 'test', 3]
        }

        serializer = OrderIdsSerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('order_ids', serializer.errors)
