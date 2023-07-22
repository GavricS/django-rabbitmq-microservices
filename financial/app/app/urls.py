from django.contrib import admin
from django.urls import path, re_path
from django.views.debug import default_urlconf
from .views import InvoiceListCreateView, InvoiceRetrieveUpdateDestroyView, update_delete_invoice_by_order_id

urlpatterns = [
    re_path(r"^admin/?", admin.site.urls),# TODO remove?
    re_path(r"^api/v1/invoices/?$", InvoiceListCreateView.as_view(), name="invoice-list-create"),
    re_path(r"^api/v1/invoices/(?P<pk>\d+)/?$", InvoiceRetrieveUpdateDestroyView.as_view(), name="invoice-retrieve-update-destroy"),
    re_path(r"^api/v1/invoices/orders/(?P<order_id>\d+)/?$", update_delete_invoice_by_order_id, name="invoice-update-delete-by-order-id"),
    # re_path(r"^api/v1/invoices/orders/(?P<order_id>\d+)/?$", delete_invoice_by_order_id, name="invoice-delete-by-order-id"),
    path("", default_urlconf)# TODO remove
]
