from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import OrderSerializer, OrderItemSerializer, OrderStatusHistorySerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-order_date')
    serializer_class = OrderSerializer

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderStatusHistoryViewSet(viewsets.ModelViewSet):
    queryset = OrderStatusHistory.objects.all().order_by('-changed_at')
    serializer_class = OrderStatusHistorySerializer

def orders_dashboard(request):
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status__in=['draft', 'confirmed']).count()
    completed_orders = Order.objects.filter(status='delivered').count()

    # Calculate total revenue by summing final_amount for each delivered order
    delivered_orders = Order.objects.filter(status='delivered')
    total_revenue = sum(order.final_amount for order in delivered_orders)

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'orders/dashboard.html', context)
