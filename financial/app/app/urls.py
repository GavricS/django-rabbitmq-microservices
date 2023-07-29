from django.contrib import admin
from django.urls import re_path
from .views import InvoiceListCreateView, InvoiceRetrieveUpdateDestroyView, UpdateDeleteInvoiceByOrderIdView

urlpatterns = [
    re_path(r"^api/v1/invoices/?$", InvoiceListCreateView.as_view(), name="invoice-list-create"),
    re_path(r"^api/v1/invoices/(?P<pk>\d+)/?$", InvoiceRetrieveUpdateDestroyView.as_view(), name="invoice-retrieve-update-destroy"),
    re_path(r"^api/v1/invoices/orders/(?P<order_id>\d+)/?$", UpdateDeleteInvoiceByOrderIdView.as_view(), name="invoice-update-delete-by-order-id"),
]
