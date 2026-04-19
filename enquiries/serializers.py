from rest_framework import serializers
from .models import Enquiry, EnquiryItem, EnquiryFollowUp

class EnquiryItemSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = EnquiryItem
        fields = '__all__'

class EnquiryFollowUpSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)

    class Meta:
        model = EnquiryFollowUp
        fields = '__all__'

class EnquirySerializer(serializers.ModelSerializer):
    items = EnquiryItemSerializer(many=True, read_only=True)
    follow_ups = EnquiryFollowUpSerializer(many=True, read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Enquiry
        fields = '__all__'