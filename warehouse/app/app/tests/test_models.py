from django.test import TestCase
from app.models import Product
from django.db.utils import DataError

class ProductModelTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            stock=1000,
            price=1000
        )

    def test_product_creation_ok(self):
        product = Product.objects.create(
            stock=2000,
            price=2000
        )

        self.assertTrue(isinstance(product, Product))
        self.assertEqual(product.stock, 2000)
        self.assertEqual(product.price, 2000)

    def test_product_creation_negative_stock_fail(self):
        with self.assertRaises(DataError):
            product = Product.objects.create(
                stock=-12345,
                price=1000
            )

    def test_product_creation_negative_price_fail(self):
        with self.assertRaises(DataError):
            product = Product.objects.create(
                stock=12345,
                price=-1000
            )

    def test_get_product_ok(self):
        retrieved_product = Product.objects.get(pk=self.product.pk)

        self.assertEqual(retrieved_product, self.product)

    def test_delete_product_ok(self):
        product_to_delete = Product.objects.get(pk=self.product.pk)

        product_to_delete.delete()

        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.pk)

    def test_update_product_ok(self):
        updated_stock = 5
        self.product.stock = updated_stock

        self.product.save()

        updated_product = Product.objects.get(pk=self.product.pk)
        self.assertEqual(updated_product.stock, updated_stock)

    def test_update_product_non_integer_stock_fail(self):
        with self.assertRaises(ValueError):
            self.product.stock = 'test'
            self.product.save()

    def test_update_product_non_integer_price_fail(self):
        with self.assertRaises(ValueError):
            self.product.price = 'test'
            self.product.save()

    def test_update_product_negative_stock_fail(self):
        with self.assertRaises(DataError):
            self.product.stock = -12345
            self.product.save()

    def test_update_product_negative_price_fail(self):
        with self.assertRaises(DataError):
            self.product.price = -500
            self.product.save()
