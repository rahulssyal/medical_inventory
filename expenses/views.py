from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from rest_framework import viewsets
from .models import Expense, ExpenseCategory, DailyExpense
from .serializers import ExpenseSerializer, ExpenseCategorySerializer, DailyExpenseSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all().order_by('-expense_date')
    serializer_class = ExpenseSerializer

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer

class DailyExpenseViewSet(viewsets.ModelViewSet):
    queryset = DailyExpense.objects.all().order_by('-date')
    serializer_class = DailyExpenseSerializer

def expenses_dashboard(request):
    total_expenses = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    pending_approvals = Expense.objects.filter(is_approved=False).count()
    this_month_expenses = Expense.objects.filter(
        expense_date__month=timezone.now().month,
        expense_date__year=timezone.now().year
    ).aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_expenses': total_expenses,
        'pending_approvals': pending_approvals,
        'this_month_expenses': this_month_expenses,
    }
    return render(request, 'expenses/dashboard.html', context)
