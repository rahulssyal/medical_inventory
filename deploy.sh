#!/bin/bash
# Deployment preparation script for Medical Inventory Management System

echo "🚀 Preparing for deployment..."

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if needed (optional)
echo "👤 Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

echo "✅ Deployment preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Commit your changes to Git"
echo "2. Push to your Git repository"
echo "3. Deploy to your chosen platform"
echo ""
echo "🔗 Popular free hosting options:"
echo "- Railway: https://railway.app"
echo "- Render: https://render.com"
echo "- Fly.io: https://fly.io"
echo "- PythonAnywhere: https://www.pythonanywhere.com"