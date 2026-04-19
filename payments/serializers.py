from rest_framework import serializers
from .models import Payment, Receipt, PaymentReminder

class PaymentSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    received_by_name = serializers.CharField(source='received_by.username', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    payment_number = serializers.CharField(source='payment.payment_number', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.username', read_only=True)

    class Meta:
        model = Receipt
        fields = '__all__'

class PaymentReminderSerializer(serializers.ModelSerializer):
    order_number = serializers.CharField(source='order.order_number', read_only=True)
    sent_by_name = serializers.CharField(source='sent_by.username', read_only=True)

    class Meta:
        model = PaymentReminder
        fields = '__all__'