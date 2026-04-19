from django.shortcuts import render
from rest_framework import viewsets
from .models import Event, MarketingCampaign, Lead
from .serializers import EventSerializer, MarketingCampaignSerializer, LeadSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-start_date')
    serializer_class = EventSerializer

class MarketingCampaignViewSet(viewsets.ModelViewSet):
    queryset = MarketingCampaign.objects.all().order_by('-start_date')
    serializer_class = MarketingCampaignSerializer

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all().order_by('-created_at')
    serializer_class = LeadSerializer

def marketing_dashboard(request):
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(status__in=['planned', 'confirmed']).count()
    active_campaigns = MarketingCampaign.objects.filter(status='active').count()
    total_leads = Lead.objects.count()

    context = {
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'active_campaigns': active_campaigns,
        'total_leads': total_leads,
    }
    return render(request, 'marketing/dashboard.html', context)
