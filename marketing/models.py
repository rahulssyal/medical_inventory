from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    EVENT_TYPES = [
        ('conference', 'Medical Conference'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('trade_show', 'Trade Show'),
        ('webinar', 'Webinar'),
        ('meeting', 'Business Meeting'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    venue_details = models.TextField(blank=True)
    expected_attendees = models.PositiveIntegerField(null=True, blank=True)
    actual_attendees = models.PositiveIntegerField(null=True, blank=True)
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.start_date.date()}"

class MarketingCampaign(models.Model):
    CAMPAIGN_TYPES = [
        ('email', 'Email Campaign'),
        ('social_media', 'Social Media'),
        ('advertisement', 'Advertisement'),
        ('partnership', 'Partnership'),
        ('promotion', 'Product Promotion'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=200)
    campaign_type = models.CharField(max_length=20, choices=CAMPAIGN_TYPES)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    target_audience = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    actual_revenue = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    results = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Lead(models.Model):
    SOURCE_CHOICES = [
        ('event', 'Event'),
        ('campaign', 'Marketing Campaign'),
        ('referral', 'Referral'),
        ('website', 'Website'),
        ('cold_call', 'Cold Call'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal', 'Proposal Sent'),
        ('negotiation', 'Negotiation'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    source_details = models.TextField(blank=True)  # Specific event or campaign
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.status}"
