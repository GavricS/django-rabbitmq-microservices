from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json

class ProductAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        data = {
            'stock': 500,
            'price': 1000,
        }
        response = self.create_product(data)
        self.product = json.loads(response.content)

    def create_product(self, data):
        return self.client.post(reverse('product-list-create'), data, format='json')

    def test_create_product_ok(self):
        data = {
            'stock': 1000,
            'price': 200,
        }

        response = self.create_product(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_stock_fail(self):
        data = {
            'price': 1000,
        }

        response = self.create_product(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_missing_price_fail(self):
        data = {
            'stock': 1000,
        }

        response = self.create_product(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_negative_stock_fail(self):
        data = {
            'stock': -1000,
            'price': 1000,
        }

        response = self.create_product(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_negative_price_fail(self):
        data = {
            'stock': 1000,
            'price': -1000,
        }

        response = self.create_product(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_non_integer_stock_fail(self):
        data = {
            'stock': 'a',
            'price': 1000,
        }

        response = self.create_product(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_non_integer_price_fail(self):
        data = {
            'stock': 1000,
            'price': 'test',
        }

        response = self.create_product(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_products_ok(self):
        response = self.client.get(reverse('product-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [self.product])

    def test_retrieve_product_ok(self):
        response = self.client.get(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.product)

    def test_retrieve_product_not_found_fail(self):
        response = self.client.get(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id'] + 1}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_ok(self):
        updated_data = {
            'stock': 2000,
            'price': 1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = updated_data
        response_data['id'] = self.product['id']
        self.assertEqual(response.data, response_data)

    def test_update_product_not_found_fail(self):
        updated_data = {
            'stock': 2000,
            'price': 1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id'] + 1}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_missing_stock_fail(self):
        updated_data = {
            'price': 1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_missing_price_fail(self):
        updated_data = {
            'stock': 2000,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_negative_stock_fail(self):
        updated_data = {
            'stock': -2000,
            'price': 1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_negative_price_fail(self):
        updated_data = {
            'stock': 2000,
            'price': -1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_negative_stock_fail(self):
        updated_data = {
            'stock': -2000,
            'price': 1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_negative_price_fail(self):
        updated_data = {
            'stock': 2000,
            'price': -1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_non_integer_stock_fail(self):
        updated_data = {
            'stock': 'test',
            'price': 1500,
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_non_integer_price_fail(self):
        updated_data = {
            'stock': 2000,
            'price': 'test',
        }

        response = self.client.put(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_product_ok(self):
        response = self.client.delete(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_not_found_fail(self):
        response = self.client.delete(reverse('product-retrieve-update-destroy', kwargs={'pk': self.product['id'] + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_update_stock_increase_ok(self):
        data = {
            'quantity': 2
        }

        response = self.client.put(reverse('product-update-stock', kwargs={'pk': self.product['id']}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = {
            'id': self.product['id'],
            'stock': 502,
            'price': 1000
        }
        self.assertEqual(response.data, response_data)

    def test_product_update_stock_decrease_ok(self):
        data = {
            'quantity': -2
        }

        response = self.client.put(reverse('product-update-stock', kwargs={'pk': self.product['id']}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = {
            'id': self.product['id'],
            'stock': 498,
            'price': 1000
        }
        self.assertEqual(response.data, response_data)

    def test_product_update_stock_not_found_fail(self):
        data = {
            'quantity': 2
        }

        response = self.client.put(reverse('product-update-stock', kwargs={'pk': self.product['id'] + 1}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_product_update_stock_missing_quantity_fail(self):
        data = {}

        response = self.client.put(reverse('product-update-stock', kwargs={'pk': self.product['id']}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_update_stock_non_integer_quantity_fail(self):
        data = {
            'quantity': 'test'
        }

        response = self.client.put(reverse('product-update-stock', kwargs={'pk': self.product['id']}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
