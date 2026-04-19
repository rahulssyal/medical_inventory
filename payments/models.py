from django.db import models
from django.contrib.auth.models import User
from orders.models import Order

class Payment(models.Model):
    PAYMENT_TYPES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('online', 'Online Payment'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_number = models.CharField(max_length=50, unique=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    reference_number = models.CharField(max_length=100, blank=True)  # Transaction ID, cheque number, etc.
    notes = models.TextField(blank=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.payment_number} - {self.amount}"

class Receipt(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    receipt_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateTimeField(auto_now_add=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    customer_copy = models.BooleanField(default=True)
    office_copy = models.BooleanField(default=True)

    def __str__(self):
        return f"Receipt {self.receipt_number}"

class PaymentReminder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_reminders')
    reminder_date = models.DateTimeField()
    amount_due = models.DecimalField(max_digits=12, decimal_places=2)
    message = models.TextField()
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment reminder for {self.order.order_number} - {self.amount_due}"
