from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from .views import ServiceViewSet, OrdersViewSet

router = DefaultRouter()
router.register(r"services", ServiceViewSet, basename="services")
router.register(r'orders', OrdersViewSet, basename='orders_crud')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
