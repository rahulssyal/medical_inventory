from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Equipment
from enquiries.models import Enquiry
from orders.models import Order, OrderItem
from payments.models import Payment
from marketing.models import Event, Lead
from expenses.models import ExpenseCategory, Expense
from datetime import date, datetime

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories = [
            Category.objects.create(name='Respiratory Equipment', description='Oxygen cylinders, ventilators, etc.'),
            Category.objects.create(name='Monitoring Equipment', description='Patient monitors, ECG machines'),
            Category.objects.create(name='Surgical Equipment', description='Surgical tools and equipment'),
            Category.objects.create(name='Mobility Aids', description='Wheelchairs, walkers, etc.'),
            Category.objects.create(name='Diagnostic Equipment', description='Ultrasound, X-ray machines'),
        ]

        # Create suppliers
        suppliers = [
            Supplier.objects.create(
                name='MedTech Solutions',
                contact_person='John Smith',
                email='john@medtech.com',
                phone='+1-555-0101',
                address='123 Medical Street, Health City, HC 12345'
            ),
            Supplier.objects.create(
                name='Global Health Corp',
                contact_person='Sarah Johnson',
                email='sarah@globalhealth.com',
                phone='+1-555-0102',
                address='456 Wellness Ave, Care Town, CT 67890'
            ),
        ]

        # Create equipment
        equipment_data = [
            {
                'name': 'Oxygen Cylinder (10L)',
                'category': categories[0],
                'equipment_type': 'oxygen_cylinder',
                'model_number': 'O2-10L-001',
                'serial_number': 'O2CYL001',
                'supplier': suppliers[0],
                'purchase_price': 150.00,
                'selling_price': 200.00,
                'quantity_in_stock': 25,
                'minimum_stock_level': 10,
                'location': 'Warehouse A',
            },
            {
                'name': 'Patient Monitor',
                'category': categories[1],
                'equipment_type': 'monitor',
                'model_number': 'PM-500',
                'serial_number': 'MON001',
                'supplier': suppliers[1],
                'purchase_price': 1200.00,
                'selling_price': 1600.00,
                'quantity_in_stock': 8,
                'minimum_stock_level': 3,
                'location': 'Warehouse B',
            },
            {
                'name': 'Wheelchair (Manual)',
                'category': categories[3],
                'equipment_type': 'wheelchair',
                'model_number': 'WC-M-001',
                'serial_number': 'WHL001',
                'supplier': suppliers[0],
                'purchase_price': 300.00,
                'selling_price': 450.00,
                'quantity_in_stock': 15,
                'minimum_stock_level': 5,
                'location': 'Warehouse A',
            },
        ]

        for eq_data in equipment_data:
            Equipment.objects.create(**eq_data)

        # Create expense categories
        expense_categories = [
            ExpenseCategory.objects.create(name='Office Supplies', description='Paper, pens, etc.'),
            ExpenseCategory.objects.create(name='Travel', description='Transportation and accommodation'),
            ExpenseCategory.objects.create(name='Marketing', description='Advertising and promotions'),
            ExpenseCategory.objects.create(name='Utilities', description='Electricity, water, internet'),
        ]

        # Create sample expenses
        Expense.objects.create(
            title='Office Stationery',
            description='Monthly office supplies',
            category=expense_categories[0],
            expense_type='operational',
            amount=150.00,
            payment_method='cash',
            expense_date=date.today(),
            vendor='Office Depot',
            incurred_by=User.objects.get(username='admin'),
            is_approved=True,
            approval_date=datetime.now(),
        )

        # Create sample enquiry
        enquiry = Enquiry.objects.create(
            customer_name='Dr. Robert Wilson',
            customer_email='robert.wilson@hospital.com',
            customer_phone='+1-555-0199',
            customer_address='789 Hospital Road, Medical City, MC 11111',
            enquiry_number='ENQ001',
            status='completed',
            priority='high',
            description='Need oxygen cylinders and patient monitors for new ICU wing',
            assigned_to=User.objects.get(username='admin'),
        )

        # Create sample order
        order = Order.objects.create(
            order_number='ORD001',
            enquiry=enquiry,
            customer_name=enquiry.customer_name,
            customer_email=enquiry.customer_email,
            customer_phone=enquiry.customer_phone,
            customer_address=enquiry.customer_address,
            status='delivered',
            payment_status='paid',
            total_amount=1800.00,
            tax_amount=180.00,
            order_date=datetime.now(),
            actual_delivery_date=date.today(),
            created_by=User.objects.get(username='admin'),
        )

        # Create order items
        oxygen_cylinder = Equipment.objects.get(serial_number='O2CYL001')
        monitor = Equipment.objects.get(serial_number='MON001')

        OrderItem.objects.create(
            order=order,
            equipment=oxygen_cylinder,
            quantity=2,
            unit_price=oxygen_cylinder.selling_price,
        )

        OrderItem.objects.create(
            order=order,
            equipment=monitor,
            quantity=1,
            unit_price=monitor.selling_price,
        )

        # Create payment
        Payment.objects.create(
            order=order,
            payment_number='PAY001',
            payment_type='bank_transfer',
            amount=1980.00,  # Including tax
            payment_date=datetime.now(),
            status='completed',
            reference_number='BT001234',
            received_by=User.objects.get(username='admin'),
        )

        # Create sample event
        Event.objects.create(
            title='Medical Equipment Expo 2026',
            event_type='trade_show',
            description='Annual medical equipment trade show',
            start_date=datetime(2026, 6, 15, 9, 0),
            end_date=datetime(2026, 6, 17, 17, 0),
            location='Convention Center, Tech City',
            expected_attendees=500,
            budget=5000.00,
            status='planned',
            organizer=User.objects.get(username='admin'),
        )

        # Create sample lead
        Lead.objects.create(
            name='Dr. Emily Chen',
            email='emily.chen@clinic.com',
            phone='+1-555-0200',
            company='City General Hospital',
            source='event',
            source_details='Medical Equipment Expo 2025',
            status='qualified',
            estimated_value=5000.00,
            notes='Interested in ventilator systems',
            assigned_to=User.objects.get(username='admin'),
        )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.stdout.write('Sample data includes:')
        self.stdout.write('- 5 equipment categories')
        self.stdout.write('- 2 suppliers')
        self.stdout.write('- 3 equipment items')
        self.stdout.write('- 1 enquiry and order with payment')
        self.stdout.write('- 1 marketing event and lead')
        self.stdout.write('- Sample expenses')