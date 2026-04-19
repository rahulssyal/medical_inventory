"""
Production settings for Medical Inventory Management System
Override development settings for production deployment
"""

import os
import dj_database_url
from .settings import *

# Security settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('The SECRET_KEY environment variable must be set in production.')

# Allowed hosts - update with your domain
ALLOWED_HOSTS = [
    'your-app-name.onrender.com',  # For Render
    'medicalinventory-production.up.railway.app',  # Your Railway domain
    'your-domain.com',  # Your custom domain
    'localhost',
    '127.0.0.1',
]

# Dynamically add Railway and other deployment hosts
deployment_hosts = os.environ.get('ALLOWED_HOSTS', '')
if deployment_hosts:
    ALLOWED_HOSTS.extend([host.strip() for host in deployment_hosts.split(',')])

# Add Railway domain if available
railway_domain = os.environ.get('RAILWAY_STATIC_URL', '').replace('https://', '').replace('http://', '')
if railway_domain:
    ALLOWED_HOSTS.append(railway_domain)

# For Railway, also try to get the domain from other env vars
railway_project_domain = os.environ.get('RAILWAY_PROJECT_DOMAIN')
if railway_project_domain:
    ALLOWED_HOSTS.append(railway_project_domain)

# Add any allowed hosts from environment variables
allowed_hosts_env = os.environ.get('ALLOWED_HOSTS', '')
if allowed_hosts_env:
    ALLOWED_HOSTS.extend([host.strip() for host in allowed_hosts_env.split(',') if host.strip()])

# Database - switch to PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'medical_inventory'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require' if os.environ.get('DB_SSL', 'false').lower() == 'true' else 'disable',
        }
    }
}

database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES['default'] = dj_database_url.parse(database_url, conn_max_age=600, ssl_require=True)

# Static files for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# WhiteNoise for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://your-frontend-domain.com",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Email settings (configure for production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}