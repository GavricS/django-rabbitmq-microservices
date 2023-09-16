from django.test import TestCase
from app.models import Order
from django.db.utils import DataError

class OrderModelTestCase(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            product_id=12345,
            quantity=2,
            price=1000
        )

    def test_order_creation_ok(self):
        order = Order.objects.create(
            product_id=12345,
            quantity=2,
            price=1000
        )

        self.assertTrue(isinstance(order, Order))
        self.assertEqual(order.product_id, 12345)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.price, 1000)

    def test_order_creation_negative_product_id_fail(self):
        with self.assertRaises(DataError):
            order = Order.objects.create(
                product_id=-12345,
                quantity=2,
                price=1000
            )

    def test_order_creation_negative_quantity_fail(self):
        with self.assertRaises(DataError):
            order = Order.objects.create(
                product_id=12345,
                quantity=-2,
                price=1000
            )

    def test_order_creation_negative_price_fail(self):
        with self.assertRaises(DataError):
            order = Order.objects.create(
                product_id=12345,
                quantity=2,
                price=-1000
            )

    def test_get_order_ok(self):
        retrieved_order = Order.objects.get(pk=self.order.pk)

        self.assertEqual(retrieved_order, self.order)

    def test_delete_order_ok(self):
        order_to_delete = Order.objects.get(pk=self.order.pk)

        order_to_delete.delete()

        with self.assertRaises(Order.DoesNotExist):
            Order.objects.get(id=self.order.pk)

    def test_update_order_ok(self):
        updated_quantity = 5
        self.order.quantity = updated_quantity

        self.order.save()

        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(updated_order.quantity, updated_quantity)

    def test_update_order_non_integer_product_id_fail(self):
        with self.assertRaises(ValueError):
            self.order.product_id = 'test'
            self.order.save()

    def test_update_order_non_integer_quantity_fail(self):
        with self.assertRaises(ValueError):
            self.order.quantity = 'test'
            self.order.save()

    def test_update_order_non_integer_price_fail(self):
        with self.assertRaises(ValueError):
            self.order.price = 'test'
            self.order.save()

    def test_update_order_negative_product_id_fail(self):
        with self.assertRaises(DataError):
            self.order.product_id = -12345
            self.order.save()

    def test_update_order_negative_quantity_fail(self):
        with self.assertRaises(DataError):
            self.order.quantity = -5
            self.order.save()

    def test_update_order_negative_price_fail(self):
        with self.assertRaises(DataError):
            self.order.price = -500
            self.order.save()
