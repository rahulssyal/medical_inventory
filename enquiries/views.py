from django.shortcuts import render
from rest_framework import viewsets
from .models import Enquiry, EnquiryItem, EnquiryFollowUp
from .serializers import EnquirySerializer, EnquiryItemSerializer, EnquiryFollowUpSerializer

class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all().order_by('-created_at')
    serializer_class = EnquirySerializer

class EnquiryItemViewSet(viewsets.ModelViewSet):
    queryset = EnquiryItem.objects.all()
    serializer_class = EnquiryItemSerializer

class EnquiryFollowUpViewSet(viewsets.ModelViewSet):
    queryset = EnquiryFollowUp.objects.all().order_by('-created_at')
    serializer_class = EnquiryFollowUpSerializer

def enquiries_dashboard(request):
    total_enquiries = Enquiry.objects.count()
    pending_enquiries = Enquiry.objects.filter(status='pending').count()
    completed_enquiries = Enquiry.objects.filter(status='completed').count()

    context = {
        'total_enquiries': total_enquiries,
        'pending_enquiries': pending_enquiries,
        'completed_enquiries': completed_enquiries,
    }
    return render(request, 'enquiries/dashboard.html', context)
