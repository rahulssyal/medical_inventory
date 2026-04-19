from django.shortcuts import render
from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Supplier, Equipment, StockMovement
from .serializers import (
    CategorySerializer, SupplierSerializer,
    EquipmentSerializer, StockMovementSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        equipment = self.get_object()
        quantity = request.data.get('quantity', 0)
        movement_type = request.data.get('movement_type')
        reason = request.data.get('reason', '')

        if movement_type not in ['in', 'out', 'adjustment']:
            return Response(
                {'error': 'Invalid movement type'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create stock movement record
        StockMovement.objects.create(
            equipment=equipment,
            movement_type=movement_type,
            quantity=quantity if movement_type == 'in' else -abs(quantity),
            reason=reason,
            performed_by=request.user
        )

        # Update equipment stock
        if movement_type == 'in':
            equipment.quantity_in_stock += quantity
        elif movement_type == 'out':
            if equipment.quantity_in_stock < quantity:
                return Response(
                    {'error': 'Insufficient stock'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            equipment.quantity_in_stock -= quantity
        else:  # adjustment
            equipment.quantity_in_stock = quantity

        equipment.save()

        serializer = self.get_serializer(equipment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_items = Equipment.objects.filter(
            quantity_in_stock__lte=models.F('minimum_stock_level')
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all().order_by('-created_at')
    serializer_class = StockMovementSerializer

# Template views for Django templates (alternative to React)
def inventory_dashboard(request):
    total_equipment = Equipment.objects.count()
    low_stock_count = Equipment.objects.filter(
        quantity_in_stock__lte=models.F('minimum_stock_level')
    ).count()
    total_value = Equipment.objects.aggregate(
        total=models.Sum(models.F('quantity_in_stock') * models.F('selling_price'))
    )['total'] or 0

    context = {
        'total_equipment': total_equipment,
        'low_stock_count': low_stock_count,
        'total_value': total_value,
    }
    return render(request, 'inventory/dashboard.html', context)

def equipment_list(request):
    equipment = Equipment.objects.all()
    return render(request, 'inventory/equipment_list.html', {'equipment': equipment})
