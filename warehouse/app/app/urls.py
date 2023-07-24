from django.contrib import admin
from django.views.debug import default_urlconf
from django.urls import path, re_path
from .views import ProductListCreateView, ProductRetrieveUpdateDestroyView, UpdateProductStockView

urlpatterns = [
    re_path(r"^admin/?", admin.site.urls),# TODO remove?
    re_path(r"^api/v1/products/?$", ProductListCreateView.as_view(), name="product-list-create"),
    re_path(r"^api/v1/products/(?P<pk>\d+)/?$", ProductRetrieveUpdateDestroyView.as_view(), name="product-retrieve-update-destroy"),
    re_path(r"^api/v1/products/stock/(?P<pk>\d+)/?$", UpdateProductStockView.as_view(), name="product-update-stock"),
    path("", default_urlconf)# TODO remove
]
