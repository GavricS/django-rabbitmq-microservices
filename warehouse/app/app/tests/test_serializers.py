from django.test import TestCase
from app.models import Product
from app.serializers import ProductSerializer, ProductQuantitySerializer

class ProductSerializerTestCase(TestCase):
    def test_product_serializer_ok(self):
        product_data = {
            'id': 1,
            'stock': 10,
            'price': 100
        }
        product = Product.objects.create(**product_data)

        serializer = ProductSerializer(product)

        serialized_data = serializer.data
        self.assertEqual(serialized_data, product_data)

class ProductQuantitySerializerTestCase(TestCase):
    def test_product_quantity_serializer_ok(self):
        input_data = {'quantity': 5}

        serializer = ProductQuantitySerializer(data=input_data)
        self.assertTrue(serializer.is_valid())

        validated_data = serializer.validated_data
        self.assertEqual(validated_data['quantity'], input_data['quantity'])

    def test_product_quantity_serializer_missing_quantity_fail(self):
        input_data = {}

        serializer = ProductQuantitySerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)

    def test_product_quantity_serializer_non_integer_quantity_fail(self):
        input_data = {'quantity': 'test'}

        serializer = ProductQuantitySerializer(data=input_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('quantity', serializer.errors)
