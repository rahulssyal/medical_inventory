from rest_framework import serializers
from .models import Expense, ExpenseCategory, DailyExpense

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)
    incurred_by_name = serializers.CharField(source='incurred_by.username', read_only=True)

    class Meta:
        model = Expense
        fields = '__all__'

class DailyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyExpense
        fields = '__all__'