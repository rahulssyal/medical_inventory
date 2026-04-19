from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'payments', views.PaymentViewSet)
router.register(r'receipts', views.ReceiptViewSet)
router.register(r'payment-reminders', views.PaymentReminderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.payments_dashboard, name='payments_dashboard'),
]