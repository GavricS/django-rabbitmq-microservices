from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json

class OrderAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        data = {
            'product_id': 1,
            'quantity': 5,
            'price': 1000,
        }
        response = self.create_order(data)
        self.order = json.loads(response.content)

    def create_order(self, data):
        return self.client.post(reverse('order-list-create'), data, format='json')

    def test_create_order_ok(self):
        data = {
            'product_id': 1,
            'quantity': 5,
            'price': 1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_missing_product_id_fail(self):
        data = {
            'quantity': 5,
            'price': 1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_missing_quantity_fail(self):
        data = {
            'product_id': 1,
            'price': 1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_missing_price_fail(self):
        data = {
            'product_id': 1,
            'quantity': 5,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_negative_product_id_fail(self):
        data = {
            'product_id': -1,
            'quantity': 5,
            'price': 1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_negative_quantity_fail(self):
        data = {
            'product_id': 1,
            'quantity': -5,
            'price': 1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_negative_price_fail(self):
        data = {
            'product_id': 1,
            'quantity': 5,
            'price': -1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_non_integer_product_id_fail(self):
        data = {
            'product_id': 'a',
            'quantity': 'test',
            'price': 1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_non_integer_quantity_fail(self):
        data = {
            'product_id': 1,
            'quantity': 'test',
            'price': 1000,
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_non_integer_price_fail(self):
        data = {
            'product_id': 1,
            'quantity': 5,
            'price': 'test',
        }

        response = self.create_order(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_orders_ok(self):
        response = self.client.get(reverse('order-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [self.order])

    def test_retrieve_order_ok(self):
        response = self.client.get(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.order)

    def test_retrieve_order_not_found_fail(self):
        response = self.client.get(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id'] + 1}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_ok(self):
        updated_data = {
            'product_id': 2,
            'quantity': 10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = updated_data
        response_data['id'] = self.order['id']
        self.assertEqual(response.data, response_data)

    def test_update_order_not_found_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': 10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id'] + 1}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_order_missing_product_id_fail(self):
        updated_data = {
            'quantity': 10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_missing_quantity_fail(self):
        updated_data = {
            'product_id': 2,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_missing_price_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': 10,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_negative_product_id_fail(self):
        updated_data = {
            'product_id': -2,
            'quantity': 10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_negative_quantity_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': -10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_negative_price_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': 10,
            'price': -1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_negative_product_id_fail(self):
        updated_data = {
            'product_id': -2,
            'quantity': 10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_negative_quantity_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': -10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_negative_price_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': 10,
            'price': -1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_non_integer_product_id_fail(self):
        updated_data = {
            'product_id': 'test',
            'quantity': 10,
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_non_integer_quantity_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': 'test',
            'price': 1500,
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_order_non_integer_price_fail(self):
        updated_data = {
            'product_id': 2,
            'quantity': 10,
            'price': 'test',
        }

        response = self.client.put(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_order_ok(self):
        response = self.client.delete(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_not_found_fail(self):
        response = self.client.delete(reverse('order-retrieve-update-destroy', kwargs={'pk': self.order['id'] + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_checkout_order_ok(self):
        response = self.client.post(reverse('order-checkout', kwargs={'pk': self.order['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_checkout_order_not_found_fail(self):
        response = self.client.post(reverse('order-checkout', kwargs={'pk': self.order['id'] + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
