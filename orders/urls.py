from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
router.register(r'order-items', views.OrderItemViewSet)
router.register(r'order-status-history', views.OrderStatusHistoryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.orders_dashboard, name='orders_dashboard'),
]