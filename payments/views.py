from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets
from .models import Payment, Receipt, PaymentReminder
from .serializers import PaymentSerializer, ReceiptSerializer, PaymentReminderSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-payment_date')
    serializer_class = PaymentSerializer

class ReceiptViewSet(viewsets.ModelViewSet):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

class PaymentReminderViewSet(viewsets.ModelViewSet):
    queryset = PaymentReminder.objects.all().order_by('-reminder_date')
    serializer_class = PaymentReminderSerializer

def payments_dashboard(request):
    total_payments = Payment.objects.filter(status='completed').aggregate(
        total=Sum('amount')
    )['total'] or 0
    pending_payments = Payment.objects.filter(status='pending').count()
    overdue_payments = Payment.objects.filter(status='overdue').count()

    context = {
        'total_payments': total_payments,
        'pending_payments': pending_payments,
        'overdue_payments': overdue_payments,
    }
    return render(request, 'payments/dashboard.html', context)
