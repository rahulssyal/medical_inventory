from django.contrib import admin
from .models import Payment, Receipt, PaymentReminder

# Register your models here.

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_number', 'order', 'payment_type', 'amount', 'status', 'payment_date', 'received_by']
    list_filter = ['payment_type', 'status', 'payment_date', 'received_by']
    search_fields = ['payment_number', 'order__order_number', 'reference_number']
    ordering = ['-payment_date']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'payment', 'issued_date', 'issued_by', 'customer_copy', 'office_copy']
    list_filter = ['issued_date', 'issued_by', 'customer_copy', 'office_copy']
    search_fields = ['receipt_number', 'payment__payment_number']
    ordering = ['-issued_date']
    readonly_fields = ['issued_date']

@admin.register(PaymentReminder)
class PaymentReminderAdmin(admin.ModelAdmin):
    list_display = ['order', 'reminder_date', 'amount_due', 'sent_by', 'is_sent']
    list_filter = ['reminder_date', 'sent_by', 'is_sent']
    search_fields = ['order__order_number', 'message']
    ordering = ['-reminder_date']
    readonly_fields = ['created_at']
