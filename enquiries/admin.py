from django.contrib import admin
from .models import Enquiry, EnquiryItem, EnquiryFollowUp

# Register your models here.

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['enquiry_number', 'customer_name', 'customer_email', 'status', 'priority', 'assigned_to', 'created_at']
    list_filter = ['status', 'priority', 'assigned_to', 'created_at']
    search_fields = ['enquiry_number', 'customer_name', 'customer_email', 'customer_phone']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EnquiryItem)
class EnquiryItemAdmin(admin.ModelAdmin):
    list_display = ['enquiry', 'equipment', 'quantity_requested', 'unit_price', 'total_price']
    list_filter = ['equipment']
    search_fields = ['enquiry__enquiry_number', 'equipment__name']
    readonly_fields = ['created_at']

@admin.register(EnquiryFollowUp)
class EnquiryFollowUpAdmin(admin.ModelAdmin):
    list_display = ['enquiry', 'follow_up_date', 'performed_by', 'next_follow_up_date']
    list_filter = ['follow_up_date', 'performed_by']
    search_fields = ['enquiry__enquiry_number', 'notes']
    readonly_fields = ['created_at']
