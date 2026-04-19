from django.contrib import admin
from .models import Event, MarketingCampaign, Lead

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'start_date', 'end_date', 'status', 'organizer', 'expected_attendees']
    list_filter = ['event_type', 'status', 'start_date', 'organizer']
    search_fields = ['title', 'description', 'location']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(MarketingCampaign)
class MarketingCampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'campaign_type', 'start_date', 'end_date', 'status', 'responsible_person', 'budget']
    list_filter = ['campaign_type', 'status', 'start_date', 'responsible_person']
    search_fields = ['name', 'description', 'target_audience']
    ordering = ['-start_date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'source', 'status', 'estimated_value', 'assigned_to']
    list_filter = ['source', 'status', 'assigned_to', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
