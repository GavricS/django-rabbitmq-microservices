from django.contrib import admin
from django.urls import path, re_path
from django.views.debug import default_urlconf
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView, OrderCheckoutView

urlpatterns = [
    re_path(r"^admin/?", admin.site.urls),# TODO remove?
    re_path(r"^api/v1/orders/?$", OrderListCreateView.as_view(), name="order-list-create"),
    re_path(r"^api/v1/orders/(?P<pk>\d+)/?$", OrderRetrieveUpdateDestroyView.as_view(), name="order-retrieve-update-destroy"),
    re_path(r"^api/v1/orders/checkout/(?P<pk>\d+)/?$", OrderCheckoutView.as_view(), name="order-checkout"),
    path("", default_urlconf)# TODO remove
]
