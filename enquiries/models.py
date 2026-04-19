from django.db import models
from django.contrib.auth.models import User
from inventory.models import Equipment

class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    enquiry_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_close_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Enquiry {self.enquiry_number} - {self.customer_name}"

class EnquiryItem(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='items')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity_requested = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.quantity_requested}"

    @property
    def total_price(self):
        if self.unit_price:
            return self.quantity_requested * self.unit_price
        return 0

class EnquiryFollowUp(models.Model):
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, related_name='follow_ups')
    follow_up_date = models.DateTimeField()
    notes = models.TextField()
    next_follow_up_date = models.DateField(null=True, blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Follow-up for {self.enquiry.enquiry_number} on {self.follow_up_date.date()}"
