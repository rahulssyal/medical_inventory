# Medical Inventory Management System - User Manual

## 1. Overview
This Medical Inventory Management System is a Django-based application for managing medical equipment, enquiries, orders, payments, marketing events, and expenses. It includes both a web dashboard and an administrative interface.

## 2. Accessing the Application
- Open the app in your browser at: `http://127.0.0.1:8000/`
- Admin panel is available at: `http://127.0.0.1:8000/admin/`

## 3. Login Credentials
Use the default admin account for full access:
- **Username**: `admin`
- **Password**: `admin123`

> Note: This account is for development and testing only. Change passwords before production use.

## 4. Main Navigation
The main dashboard navigation includes:
- Inventory
- Enquiries
- Orders
- Payments
- Marketing
- Expenses
- Admin

Each link opens the module dashboard for quick overview and actions.

## 5. Inventory Management
Use the Inventory dashboard to manage equipment and stock.

### Features
- View equipment list and stock levels
- Track equipment categories and suppliers
- Manage stock movements for inbound and outbound inventory
- Monitor low-stock items

### Typical Workflow
1. Add categories and suppliers in the Admin panel or through the project admin.
2. Add equipment items with serial numbers, purchase and selling prices, and stock quantity.
3. Track stock movement whenever equipment is received or shipped.

## 6. Enquiries Management
Use Enquiries to record customer requests and follow-up actions.

### Features
- Create and track enquiry records
- Assign enquiries to staff
- Record enquiry items and expected values
- Manage follow-up actions and notes

### Typical Workflow
1. Create a new enquiry with customer details.
2. Add enquiry items and quantity requests.
3. Assign the enquiry to a user and update status as it progresses.
4. Record follow-up notes with dates and next steps.

## 7. Order Management
Use Orders to convert enquiries into sales and manage order lifecycle.

### Features
- Create and manage orders linked to enquiries
- Track order status and payment status
- Record shipping, taxes, and discounts
- View order item details and calculate final amount

### Typical Workflow
1. Create an order from an enquiry or manually add one.
2. Add order items and pricing details.
3. Update order status from draft to delivered.
4. Monitor payment progress as partial or completed.

## 8. Payments and Receipt Management
Use the Payments module to capture transaction details.

### Features
- Record payments for orders
- Track payment types and statuses
- Issue receipts and reminders

### Typical Workflow
1. Enter payment information when a customer pays.
2. Link the payment to an order and assign a payment number.
3. Generate a receipt if required.
4. Create reminders for overdue payments.

## 9. Marketing Management
Track events, campaigns, and leads in the Marketing dashboard.

### Features
- Manage marketing events, workshops, and webinars
- Track campaign budgets and revenue
- Store leads and follow their status

### Typical Workflow
1. Add new events and campaign details.
2. Assign responsible team members.
3. Log leads from events or campaigns.
4. Update lead status as contacts progress.

## 10. Expense Tracking
Record company expenses and daily totals.

### Features
- Manage expense categories
- Track operational and marketing costs
- Approve expenses and log receipts
- Maintain daily expense summaries

### Typical Workflow
1. Create expense categories for cost organization.
2. Add expense records with payment method and vendor details.
3. Mark expenses approved when finalized.
4. Review daily expense totals and counts.

## 11. Admin Panel
The Django admin panel is the primary management interface for all models.
- Access at: `http://127.0.0.1:8000/admin/`
- Use the same login credentials as the web app.

### Common Actions
- Add and edit inventory categories, suppliers, and equipment
- Manage enquiries, orders, payments, marketing events, and expenses
- Review and update user assignments

## 12. API Access
The app includes Django REST Framework support.
- Browsable API login is available at `http://127.0.0.1:8000/api-auth/login/`
- Use the same credentials for API access.

## 13. Running the Site Locally
To start the app locally:
1. Open a terminal in `c:\Projects\medical_inventory`
2. Run:
   ```bash
   c:/python313/python.exe manage.py runserver 8000
   ```
3. Open `http://127.0.0.1:8000/` in your browser.

## 14. Troubleshooting
- **403 CSRF verification failed**: Make sure login forms include `{% csrf_token %}` and you are using the correct login URL.
- **404 Not Found**: Verify the correct URL path and ensure the server is running.
- **Admin panel access**: Use `http://127.0.0.1:8000/admin/` and the admin credentials.

## 15. Important Notes
- This application runs in development mode by default.
- Use production settings and a proper database before deploying publicly.
- Change default credentials before allowing external access.

---

For any additional feature guidance or extensions, contact the developer or refer to the project admin documentation.