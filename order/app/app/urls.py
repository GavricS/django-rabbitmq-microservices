from django.contrib import admin
from django.urls import re_path
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView, OrderCheckoutView

urlpatterns = [
    re_path(r"^api/v1/orders/?$", OrderListCreateView.as_view(), name="order-list-create"),
    re_path(r"^api/v1/orders/(?P<pk>\d+)/?$", OrderRetrieveUpdateDestroyView.as_view(), name="order-retrieve-update-destroy"),
    re_path(r"^api/v1/orders/checkout/(?P<pk>\d+)/?$", OrderCheckoutView.as_view(), name="order-checkout"),
]
