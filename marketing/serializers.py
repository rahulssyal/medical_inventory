from rest_framework import serializers
from .models import Event, MarketingCampaign, Lead

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'

class MarketingCampaignSerializer(serializers.ModelSerializer):
    responsible_person_name = serializers.CharField(source='responsible_person.username', read_only=True)

    class Meta:
        model = MarketingCampaign
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Lead
        fields = '__all__'