# Medical Equipment Inventory Management System

A comprehensive Django-based inventory management system designed specifically for medical equipment dealers. This system provides complete workflow management from enquiry to delivery, with integrated stock management, payment tracking, and marketing tools.

## Features

### 🔐 User Authentication
- Secure login system
- Role-based access control
- Django admin panel integration

### 📦 Inventory Management
- Medical equipment cataloging (oxygen cylinders, ventilators, monitors, etc.)
- Stock level tracking with low-stock alerts
- Supplier management
- Equipment categories and classifications
- Stock movement history

### ❓ Enquiry Management
- Customer enquiry processing
- Enquiry status tracking
- Follow-up management
- Enquiry-to-order conversion

### 🛒 Order Processing
- Complete order lifecycle management
- Order status tracking (draft → confirmed → processing → shipped → delivered)
- Order item management
- Delivery tracking

### 💰 Payment & Receipt Management
- Payment processing and tracking
- Receipt generation
- Payment reminders for overdue amounts
- Multiple payment methods support

### 📈 Marketing Management
- Event planning and tracking
- Marketing campaign management
- Lead generation and tracking
- Customer relationship management

### 💸 Expense Tracking
- Daily expense recording
- Expense categorization
- Budget monitoring
- Approval workflow

## Technology Stack

- **Backend**: Django 6.0.4
- **Database**: SQLite (development) / PostgreSQL (production)
- **API**: Django REST Framework
- **Frontend**: Django Templates with Bootstrap 5
- **Authentication**: Django Auth + Token Authentication

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd your-project-directory
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data (optional)**
   ```bash
   python manage.py populate_sample_data
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/
     - Username: admin
     - Password: admin123 (if using sample data)
   - API endpoints: http://127.0.0.1:8000/[app]/api/

## Sample Data

The system includes a management command to populate sample data for testing:

```bash
python manage.py populate_sample_data
```

This creates:
- 5 equipment categories (Respiratory, Monitoring, Surgical, Mobility, Diagnostic)
- 2 suppliers
- 3 equipment items (Oxygen cylinders, Patient monitors, Wheelchairs)
- Sample enquiry, order, and payment records
- Marketing event and lead
- Sample expenses

**Default admin credentials:**
- Username: `admin`
- Password: `admin123`

## API Endpoints

### Inventory Management
- `GET/POST /inventory/api/equipment/` - Equipment CRUD
- `GET/POST /inventory/api/categories/` - Categories CRUD
- `GET/POST /inventory/api/suppliers/` - Suppliers CRUD
- `GET/POST /inventory/api/stock-movements/` - Stock movements

### Enquiry Management
- `GET/POST /enquiries/api/enquiries/` - Enquiries CRUD
- `GET/POST /enquiries/api/enquiry-items/` - Enquiry items
- `GET/POST /enquiries/api/enquiry-follow-ups/` - Follow-ups

### Order Management
- `GET/POST /orders/api/orders/` - Orders CRUD
- `GET/POST /orders/api/order-items/` - Order items
- `GET/POST /orders/api/order-status-history/` - Status history

### Payment Management
- `GET/POST /payments/api/payments/` - Payments CRUD
- `GET/POST /payments/api/receipts/` - Receipts
- `GET/POST /payments/api/payment-reminders/` - Payment reminders

### Marketing Management
- `GET/POST /marketing/api/events/` - Events CRUD
- `GET/POST /marketing/api/campaigns/` - Campaigns CRUD
- `GET/POST /marketing/api/leads/` - Leads CRUD

### Expense Tracking
- `GET/POST /expenses/api/expenses/` - Expenses CRUD
- `GET/POST /expenses/api/expense-categories/` - Categories
- `GET/POST /expenses/api/daily-expenses/` - Daily expenses

## Database Configuration

### Development (SQLite)
The project is configured to use SQLite by default for development.

### Production (PostgreSQL)
To use PostgreSQL in production, update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'medical_inventory_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Install PostgreSQL adapter:
```bash
pip install psycopg2-binary
```

## Usage Guide

### 1. Initial Setup
1. Access the admin panel at `/admin/`
2. Create categories, suppliers, and initial equipment
3. Set up user accounts and permissions

### 2. Daily Operations
1. **Inventory Management**: Add new equipment, update stock levels
2. **Enquiry Processing**: Record customer enquiries and follow up
3. **Order Processing**: Convert enquiries to orders, track fulfillment
4. **Payment Handling**: Record payments and generate receipts
5. **Expense Tracking**: Log daily expenses and monitor budgets

### 3. Reporting
- Use Django admin for basic reporting
- API endpoints provide data for custom dashboards
- Export capabilities available through admin interface

## Security Features

- CSRF protection
- SQL injection prevention
- XSS protection
- Secure password hashing
- Session management
- CORS configuration for API access

## Development

### Adding New Features
1. Create models in respective app `models.py`
2. Create serializers in `serializers.py`
3. Add views in `views.py`
4. Register URLs in `urls.py`
5. Run migrations: `python manage.py makemigrations && python manage.py migrate`

### Testing
```bash
python manage.py test
```

### Code Style
Follow Django and Python best practices. Use meaningful variable names and add docstrings to functions.

## Deployment

For production deployment:
1. Set `DEBUG = False` in settings
2. Configure production database
3. Set up static file serving
4. Use a production WSGI server (Gunicorn, uWSGI)
5. Configure web server (Nginx, Apache)
6. Set up SSL certificates
7. Configure environment variables for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper documentation
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the Django documentation
- Review the API documentation
- Contact the development team

---

**Note**: This system is designed for medical equipment dealers but can be adapted for other inventory management needs with appropriate modifications.