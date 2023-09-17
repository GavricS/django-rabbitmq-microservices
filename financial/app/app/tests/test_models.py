from django.test import TestCase
from app.models import Invoice
from django.db.utils import DataError

class InvoiceModelTestCase(TestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            order_id=12345,
            total=2,
            status=Invoice.StatusChoices.WAITING
        )

    def test_invoice_creation_ok(self):
        invoice = Invoice.objects.create(
            order_id=12346,
            total=2,
            status=Invoice.StatusChoices.WAITING
        )

        self.assertTrue(isinstance(invoice, Invoice))
        self.assertEqual(invoice.order_id, 12346)
        self.assertEqual(invoice.total, 2)
        self.assertEqual(invoice.status, Invoice.StatusChoices.WAITING)

    def test_invoice_creation_negative_order_id_fail(self):
        with self.assertRaises(DataError):
            invoice = Invoice.objects.create(
                order_id=-12345,
                total=2,
                status=Invoice.StatusChoices.WAITING
            )

    def test_invoice_creation_negative_total_fail(self):
        with self.assertRaises(DataError):
            invoice = Invoice.objects.create(
                order_id=12345,
                total=-2,
                status=Invoice.StatusChoices.WAITING
            )

    def test_get_invoice_ok(self):
        retrieved_invoice = Invoice.objects.get(pk=self.invoice.pk)

        self.assertEqual(retrieved_invoice, self.invoice)

    def test_delete_invoice_ok(self):
        invoice_to_delete = Invoice.objects.get(pk=self.invoice.pk)

        invoice_to_delete.delete()

        with self.assertRaises(Invoice.DoesNotExist):
            Invoice.objects.get(id=self.invoice.pk)

    def test_update_invoice_ok(self):
        updated_total = 5
        self.invoice.total = updated_total

        self.invoice.save()

        updated_invoice = Invoice.objects.get(pk=self.invoice.pk)
        self.assertEqual(updated_invoice.total, updated_total)

    def test_update_invoice_non_integer_order_id_fail(self):
        with self.assertRaises(ValueError):
            self.invoice.order_id = 'test'
            self.invoice.save()

    def test_update_invoice_non_integer_total_fail(self):
        with self.assertRaises(ValueError):
            self.invoice.total = 'test'
            self.invoice.save()

    def test_update_invoice_non_string_status_fail(self):
        with self.assertRaises(ValueError):
            self.invoice.status = 1
            self.invoice.save()

    def test_update_invoice_invalid_string_status_fail(self):
        with self.assertRaises(ValueError):
            self.invoice.status = 'test'
            self.invoice.save()

    def test_update_invoice_negative_order_id_fail(self):
        with self.assertRaises(DataError):
            self.invoice.order_id = -12345
            self.invoice.save()

    def test_update_invoice_negative_total_fail(self):
        with self.assertRaises(DataError):
            self.invoice.total = -5
            self.invoice.save()
