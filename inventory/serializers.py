from rest_framework import serializers
from .models import Category, Supplier, Equipment, StockMovement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class EquipmentSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    total_value = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Equipment
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)

    class Meta:
        model = StockMovement
        fields = '__all__'