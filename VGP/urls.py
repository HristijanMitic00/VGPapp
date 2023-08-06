"""VGP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from VGPapp.views import index, cart, remove_from_cart, add_to_cart, checkout, details, add, remove_cart, \
    success, userOrders, checkOrder, userInfo, register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path("register/", register, name="register"),
                  path('index/', index, name="index"),
                  path('cart/', cart, name="cart"),
                  path('details/<str:name>', details, name="details"),
                  path('accounts/', include('django.contrib.auth.urls')),
                  path('add_to_cart/<str:name>', add_to_cart, name="add_to_cart"),
                  path('add/', add, name="add"),
                  path('remove_cart/', remove_cart, name="remove_cart"),
                  path('remove_from_cart/<str:name>', remove_from_cart, name="remove_from_cart"),
                  path('checkout/', checkout, name="checkout"),
                  path('success', success, name="success"),
                  path('userOrders', userOrders, name="userOrders"),
                  path('userInfo', userInfo, name="userInfo"),
                  path('checkOrder/<int:id>', checkOrder, name="checkOrder")
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
