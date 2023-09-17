from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch, Mock

def setup_mock_send_request(mock_send_request, response_data=None, ok=True):
    mock_response = Mock()
    mock_response.ok = ok
    if response_data is not None:
        mock_response.json.return_value = response_data
    mock_send_request.return_value = mock_response

class OrderCreateViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('app.views.requests.post')
    def test_create_order_ok(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 1,
            'quantity': 2,
            'price': 100,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @patch('app.views.requests.post')
    def test_create_order_api_error_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request, response_data={'error': 'test'}, ok=False)
        data = {
            'id': 1,
            'quantity': 2,
            'price': 100,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/product/product_dashboard.html')
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_missing_id_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'quantity': 2,
            'price': 100,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/product/product_dashboard.html')
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_missing_quantity_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 1,
            'price': 100,
        }
        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/product/product_dashboard.html')
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_missing_price_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 1,
            'quantity': 2,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/product/product_dashboard.html')
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_non_integer_id_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 'test',
            'quantity': 2,
            'price': 100,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_non_integer_quantity_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 1,
            'quantity': 'test',
            'price': 100,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_non_integer_price_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 1,
            'quantity': 2,
            'price': 'test',
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_negative_id_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': -1,
            'quantity': 2,
            'price': 100,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_negative_quantity_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 1,
            'quantity': -1,
            'price': 100,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'error', response.content)

    @patch('app.views.requests.post')
    def test_create_order_negative_price_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request)
        data = {
            'id': 1,
            'quantity': 2,
            'price': -1,
        }

        response = self.client.post(reverse('order-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'error', response.content)

class OrderViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('app.views.requests.get')
    def test_get_orders_ok(self, mock_send_request):
        order_api_get_orders_response_data = [
            {
                "id": 1,
                "product_id": 1,
                "quantity": 2,
                "price": 200
            },
            {
                "id": 2,
                "product_id": 2,
                "quantity": 4,
                "price": 3200
            },
        ]
        setup_mock_send_request(mock_send_request, order_api_get_orders_response_data)

        response = self.client.get(reverse('order-dashboard'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/order/order_dashboard.html')
        self.assertNotIn(b'error', response.content)

    @patch('app.views.requests.get')
    def test_get_orders_api_error_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request, ok=False)

        response = self.client.get(reverse('order-dashboard'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/order/order_dashboard.html')
        self.assertIn(b'error', response.content)

class OrderCheckoutViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('app.views.requests.post')
    def test_checkout_order_ok(self, mock_send_request):
        setup_mock_send_request(mock_send_request)

        response = self.client.post(reverse('order-checkout', kwargs={'order_id': 1}))

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    @patch('app.views.requests.post')
    def test_checkout_order_api_error_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request, ok=False)

        response = self.client.post(reverse('order-checkout', kwargs={'order_id': 1}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/order/order_dashboard.html')
        self.assertIn(b'error', response.content)

class ProductViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('app.views.requests.get')
    def test_get_products_ok(self, mock_send_request):
        product_api_get_products_response_data = [
            {
                "id": 1,
                "stock": 1000,
                "price": 2
            },
            {
                "id": 2,
                "stock": 500,
                "price": 4
            },
        ]
        setup_mock_send_request(mock_send_request, product_api_get_products_response_data)

        response = self.client.get(reverse('product-dashboard'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/product/product_dashboard.html')
        self.assertNotIn(b'error', response.content)

    @patch('app.views.requests.get')
    def test_get_products_api_error_fail(self, mock_send_request):
        setup_mock_send_request(mock_send_request, ok=False)

        response = self.client.get(reverse('product-dashboard'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'app/product/product_dashboard.html')
        self.assertIn(b'error', response.content)
