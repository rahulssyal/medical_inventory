from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'expense-categories', views.ExpenseCategoryViewSet)
router.register(r'daily-expenses', views.DailyExpenseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.expenses_dashboard, name='expenses_dashboard'),
]