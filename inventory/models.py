from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Supplier(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    EQUIPMENT_TYPES = [
        ('oxygen_cylinder', 'Oxygen Cylinder'),
        ('ventilator', 'Ventilator'),
        ('monitor', 'Patient Monitor'),
        ('defibrillator', 'Defibrillator'),
        ('syringe_pump', 'Syringe Pump'),
        ('wheelchair', 'Wheelchair'),
        ('bed', 'Hospital Bed'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    model_number = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    minimum_stock_level = models.PositiveIntegerField(default=5)
    expiry_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='equipment_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.serial_number}"

    @property
    def is_low_stock(self):
        return self.quantity_in_stock <= self.minimum_stock_level

    @property
    def total_value(self):
        return self.quantity_in_stock * self.selling_price

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]

    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    quantity = models.IntegerField()  # Positive for in, negative for out
    reason = models.TextField(blank=True)
    reference_number = models.CharField(max_length=100, blank=True)  # Order number, etc.
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.movement_type} - {self.quantity}"
