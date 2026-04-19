from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'status', 'payment_status', 'final_amount', 'order_date', 'expected_delivery_date']
    list_filter = ['status', 'payment_status', 'order_date', 'expected_delivery_date']
    search_fields = ['order_number', 'customer_name', 'customer_email', 'customer_phone']
    ordering = ['-order_date']
    readonly_fields = ['order_date', 'updated_at', 'final_amount']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'equipment', 'quantity', 'unit_price', 'total_price']
    list_filter = ['equipment']
    search_fields = ['order__order_number', 'equipment__name']
    readonly_fields = ['created_at', 'total_price']

@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'status', 'changed_by', 'changed_at']
    list_filter = ['status', 'changed_by', 'changed_at']
    search_fields = ['order__order_number', 'notes']
    ordering = ['-changed_at']
    readonly_fields = ['changed_at']
