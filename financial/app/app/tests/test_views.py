from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.models import Invoice
import json

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        data = {
            'order_id': 1,
            'total': 5,
            'status': Invoice.StatusChoices.WAITING,
        }
        response = self.create_invoice(data)
        self.invoice = json.loads(response.content)

    def create_invoice(self, data):
        return self.client.post(reverse('invoice-list-create'), data, format='json')

    def test_create_invoice_ok(self):
        data = {
            'order_id': 2,
            'total': 5,
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invoice_missing_order_id_fail(self):
        data = {
            'total': 5,
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_missing_total_fail(self):
        data = {
            'order_id': 2,
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_missing_status_fail(self):
        data = {
            'order_id': 2,
            'total': 5,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_negative_order_id_fail(self):
        data = {
            'order_id': -1,
            'total': 5,
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_negative_total_fail(self):
        data = {
            'order_id': 2,
            'total': -5,
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_invalid_status_fail(self):
        data = {
            'order_id': 2,
            'total': 5,
            'status': 'test',
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_non_integer_order_id_fail(self):
        data = {
            'order_id': 'a',
            'total': 'test',
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_non_integer_total_fail(self):
        data = {
            'order_id': 2,
            'total': 'test',
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_non_string_status_fail(self):
        data = {
            'order_id': 2,
            'total': 5,
            'status': 1,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invoice_already_taken_order_id_fail(self):
        data = {
            'order_id': 1,
            'total': 5,
            'status': Invoice.StatusChoices.WAITING,
        }

        response = self.create_invoice(data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_invoices_ok(self):
        response = self.client.get(reverse('invoice-list-create'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [self.invoice])

    def test_retrieve_invoice_ok(self):
        response = self.client.get(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.invoice)

    def test_retrieve_invoice_not_found_fail(self):
        response = self.client.get(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id'] + 1}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invoice_ok(self):
        updated_data = {
            'order_id': 2,
            'total': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = updated_data
        response_data['id'] = self.invoice['id']
        self.assertEqual(response.data, response_data)

    def test_update_invoice_not_found_fail(self):
        updated_data = {
            'order_id': 2,
            'total': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id'] + 1}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invoice_missing_order_id_fail(self):
        updated_data = {
            'total': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_missing_total_fail(self):
        updated_data = {
            'order_id': 2,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_missing_status_fail(self):
        updated_data = {
            'order_id': 2,
            'total': 10,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_negative_order_id_fail(self):
        updated_data = {
            'order_id': -2,
            'total': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_negative_total_fail(self):
        updated_data = {
            'order_id': 2,
            'total': -10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_invalid_status_fail(self):
        updated_data = {
            'order_id': 2,
            'total': 10,
            'status': 'test',
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_negative_order_id_fail(self):
        updated_data = {
            'order_id': -2,
            'total': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_negative_total_fail(self):
        updated_data = {
            'order_id': 2,
            'total': -10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_non_string_status_fail(self):
        updated_data = {
            'order_id': 2,
            'total': 10,
            'status': 1,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_non_integer_order_id_fail(self):
        updated_data = {
            'order_id': 'test',
            'total': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_non_integer_total_fail(self):
        updated_data = {
            'order_id': 2,
            'total': 'test',
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_non_string_status_fail(self):
        updated_data = {
            'order_id': 2,
            'total': 10,
            'status': 'test',
        }

        response = self.client.put(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_invoice_ok(self):
        response = self.client.delete(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invoice_not_found_fail(self):
        response = self.client.delete(reverse('invoice-retrieve-update-destroy', kwargs={'pk': self.invoice['id'] + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_invoice_by_order_id_ok(self):
        response = self.client.delete(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invoice_by_order_id_not_found_fail(self):
        response = self.client.delete(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id'] + 1}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invoice_status_by_order_id_ok(self):
        updated_data = {
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, updated_data)

    def test_update_invoice_status_by_order_id_not_found_fail(self):
        updated_data = {
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id'] + 1}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_invoice_status_by_order_id_with_order_id_field_fail(self):
        updated_data = {
            'order_id': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_status_by_order_id_with_total_field_fail(self):
        updated_data = {
            'total': 10,
            'status': Invoice.StatusChoices.COMPLETE,
        }

        response = self.client.put(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_status_by_order_id_missing_status_fail(self):
        updated_data = {}

        response = self.client.put(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_status_by_order_id_invalid_status_fail(self):
        updated_data = {
            'status': 'test',
        }

        response = self.client.put(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invoice_status_by_order_id_non_string_status_fail(self):
        updated_data = {
            'order_id': 2,
            'total': 10,
            'status': 'test',
        }

        response = self.client.put(reverse('invoice-update-status-delete-by-order-id', kwargs={'order_id': self.invoice['order_id']}), updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invoices_by_order_ids_ok(self):
        data = {
            'order_ids': [self.invoice['order_id']]
        }

        response = self.client.post(reverse('invoice-get-multiple-by-order-id'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_invoices_by_order_ids_multiple_invoices_ok(self):
        data = {
            'order_id': 2,
            'total': 10,
            'status': Invoice.StatusChoices.WAITING,
        }
        response = self.create_invoice(data)

        data = {
            'order_ids': [self.invoice['order_id'], 2]
        }

        response = self.client.post(reverse('invoice-get-multiple-by-order-id'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


    def test_get_invoices_by_order_ids_no_matching_invoices_ok(self):
        data = {
            'order_ids': [self.invoice['order_id'] + 1]
        }

        response = self.client.post(reverse('invoice-get-multiple-by-order-id'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_invoices_by_order_ids_missing_order_ids_fail(self):
        data = {}

        response = self.client.post(reverse('invoice-get-multiple-by-order-id'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invoices_by_order_ids_non_array_order_ids_fail(self):
        data = {
            'order_ids': 'test'
        }

        response = self.client.post(reverse('invoice-get-multiple-by-order-id'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_invoices_by_order_ids_non_array_of_integers_order_ids_fail(self):
        data = {
            'order_ids': [1, 'test']
        }

        response = self.client.post(reverse('invoice-get-multiple-by-order-id'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
