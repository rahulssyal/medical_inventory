from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'equipment', views.EquipmentViewSet)
router.register(r'stock-movements', views.StockMovementViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.inventory_dashboard, name='inventory_dashboard'),
    path('equipment/', views.equipment_list, name='equipment_list'),
]