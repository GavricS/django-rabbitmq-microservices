from django.contrib import admin
from django.urls import path, re_path
from django.views.debug import default_urlconf
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView, order_checkout

urlpatterns = [
    re_path(r"^admin/?", admin.site.urls),# TODO remove?
    re_path(r"^api/orders/?$", OrderListCreateView.as_view(), name="order-list-create"),
    re_path(r"^api/orders/(?P<pk>\d+)/?$", OrderRetrieveUpdateDestroyView.as_view(), name="order-retrieve-update-destroy"),
    re_path(r"^api/orders/(?P<pk>\d+)/?$", OrderRetrieveUpdateDestroyView.as_view(), name="order-retrieve-update-destroy"),
    re_path(r"^api/orders/checkout/(?P<pk>\d+)/?$", order_checkout, name="order-checkout"),
    path("", default_urlconf)# TODO remove
]
