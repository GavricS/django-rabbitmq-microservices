"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.debug import default_urlconf
from .views import OrderListCreateView, OrderRetrieveUpdateDestroyView, order_checkout

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/orders', OrderListCreateView.as_view(), name='order-list-create'),
    path('api/orders/', OrderListCreateView.as_view(), name='order-list-create'),
    # path('api/orders/<int:id>', OrderRetrieveUpdateDestroyView.as_view(), name='order-retrieve-update-destroy'),
    path('api/orders/<int:id>/', OrderRetrieveUpdateDestroyView.as_view(), name='order-retrieve-update-destroy'),
    path('api/orders/checkout/<int:id>/', order_checkout, name='order-checkout'),
    path('', default_urlconf)
]
