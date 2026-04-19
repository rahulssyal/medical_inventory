from django.db import models
from django.contrib.auth.models import User

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Expense Categories"

class Expense(models.Model):
    EXPENSE_TYPES = [
        ('operational', 'Operational'),
        ('marketing', 'Marketing'),
        ('travel', 'Travel'),
        ('equipment', 'Equipment Purchase'),
        ('maintenance', 'Maintenance'),
        ('utilities', 'Utilities'),
        ('salary', 'Salary'),
        ('other', 'Other'),
    ]

    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('credit_card', 'Credit Card'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True)
    expense_type = models.CharField(max_length=20, choices=EXPENSE_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    expense_date = models.DateField()
    vendor = models.CharField(max_length=200, blank=True)
    receipt_number = models.CharField(max_length=100, blank=True)
    receipt_image = models.ImageField(upload_to='expense_receipts/', blank=True, null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='approved_expenses')
    incurred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='incurred_expenses')
    is_approved = models.BooleanField(default=False)
    approval_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

class DailyExpense(models.Model):
    date = models.DateField(unique=True)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    number_of_expenses = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Daily Expenses - {self.date}"

    class Meta:
        verbose_name_plural = "Daily Expenses"
