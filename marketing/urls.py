from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'campaigns', views.MarketingCampaignViewSet)
router.register(r'leads', views.LeadViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.marketing_dashboard, name='marketing_dashboard'),
]