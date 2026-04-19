from django.contrib import admin
from .models import ExpenseCategory, Expense, DailyExpense

# Register your models here.

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'expense_type', 'amount', 'expense_date', 'incurred_by', 'is_approved', 'approved_by']
    list_filter = ['expense_type', 'payment_method', 'is_approved', 'expense_date', 'category', 'incurred_by']
    search_fields = ['title', 'description', 'vendor', 'receipt_number']
    ordering = ['-expense_date']
    readonly_fields = ['created_at', 'updated_at', 'approval_date']

@admin.register(DailyExpense)
class DailyExpenseAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_expenses', 'number_of_expenses']
    list_filter = ['date']
    search_fields = ['notes']
    ordering = ['-date']
    readonly_fields = ['created_at', 'updated_at']
