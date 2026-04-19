from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'enquiries', views.EnquiryViewSet)
router.register(r'enquiry-items', views.EnquiryItemViewSet)
router.register(r'enquiry-follow-ups', views.EnquiryFollowUpViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('dashboard/', views.enquiries_dashboard, name='enquiries_dashboard'),
]