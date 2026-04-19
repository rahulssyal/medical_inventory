from django.contrib import admin
from .models import Category, Supplier, Equipment, StockMovement

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'contact_person', 'email', 'phone']
    search_fields = ['name', 'contact_person', 'email', 'phone']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'equipment_type', 'serial_number', 'quantity_in_stock', 'selling_price', 'is_low_stock', 'is_active']
    list_filter = ['category', 'equipment_type', 'supplier', 'is_active']
    search_fields = ['name', 'serial_number', 'model_number']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at', 'total_value']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['equipment', 'movement_type', 'quantity', 'performed_by', 'created_at']
    list_filter = ['movement_type', 'performed_by', 'created_at']
    search_fields = ['equipment__name', 'reference_number', 'reason']
    ordering = ['-created_at']
    readonly_fields = ['created_at']
