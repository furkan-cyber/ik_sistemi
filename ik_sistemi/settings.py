# Django settings for ik_sistemi project.
import os 
from pathlib import Path 
from datetime import timedelta 
from dotenv import load_dotenv 
 
load_dotenv() 
 
BASE_DIR = Path(__file__).resolve().parent.parent 
 
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-fallback-secret-key') 
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true' 
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') 
 
INSTALLED_APPS = [ 
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.messages', 
    'django.contrib.staticfiles', 
    'rest_framework', 
    'rest_framework_simplejwt', 
    'django_celery_beat', 
    'django_filters', 
    'core', 
] 
 
MIDDLEWARE = [ 
    'django.middleware.security.SecurityMiddleware', 
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware', 
    'django.middleware.common.CommonMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware', 
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 
] 
 
ROOT_URLCONF = 'ik_sistemi.urls' 
 
TEMPLATES = [ 
    { 
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        'DIRS': [os.path.join(BASE_DIR, 'core/templates')], 
        'APP_DIRS': True, 
        'OPTIONS': { 
            'context_processors': [ 
                'django.template.context_processors.debug', 
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth', 
                'django.contrib.messages.context_processors.messages', 
            ], 
        }, 
    }, 
] 
 
WSGI_APPLICATION = 'ik_sistemi.wsgi.application' 
 
DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.postgresql', 
        'NAME': 'ik_sistemi', 
        'USER': 'ik_user', 
        'PASSWORD': 'ik_password', 
        'HOST': 'localhost', 
        'PORT': '5432', 
    } 
} 
 
AUTH_PASSWORD_VALIDATORS = [ 
    { 
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', 
    }, 
    { 
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 
    }, 
    { 
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', 
    }, 
    { 
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', 
    }, 
] 
 
REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': [ 
        'rest_framework_simplejwt.authentication.JWTAuthentication', 
        'rest_framework.authentication.SessionAuthentication', 
    ], 
    'DEFAULT_PERMISSION_CLASSES': [ 
        'rest_framework.permissions.IsAuthenticated', 
    ], 
    'DEFAULT_FILTER_BACKENDS': [ 
        'django_filters.rest_framework.DjangoFilterBackend', 
    ], 
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', 
    'PAGE_SIZE': 20 
} 
 
SIMPLE_JWT = { 
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1), 
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1), 
    'ROTATE_REFRESH_TOKENS': True, 
    'BLACKLIST_AFTER_ROTATION': True, 
} 
 
LANGUAGE_CODE = 'tr-tr' 
TIME_ZONE = os.getenv('REPORT_TIMEZONE', 'Europe/Istanbul') 
USE_I18N = True 
USE_TZ = True 
 
STATIC_URL = '/static/' 
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_DIRS = [ 
    os.path.join(BASE_DIR, 'core/static'), 
] 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 
 
MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 
 
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 
 
# Celery Configuration 
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0') 
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0') 
CELERY_ACCEPT_CONTENT = ['json'] 
CELERY_TASK_SERIALIZER = 'json' 
CELERY_RESULT_SERIALIZER = 'json' 
CELERY_TIMEZONE = os.getenv('REPORT_TIMEZONE', 'Europe/Istanbul') 
 
# Email Configuration 
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend') 
EMAIL_HOST = os.getenv('EMAIL_HOST', '') 
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587)) 
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true' 
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '') 
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '') 
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost') 
 
# File Upload Configuration 
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', 10485760))  # 10MB 
ALLOWED_FILE_EXTENSIONS = os.getenv('ALLOWED_FILE_EXTENSIONS', 'pdf,docx,doc').split(',') 
 
# AI/ML Configuration 
USE_AI_PARSER = os.getenv('USE_AI_PARSER', 'True').lower() == 'true' 
AI_MODEL_NAME = os.getenv('AI_MODEL_NAME', 'bert-base-multilingual-cased') 
 
# Security Settings 
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', 'http://localhost:8000').split(',') 
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',') 
 
if not DEBUG: 
    SECURE_SSL_REDIRECT = True 
    SESSION_COOKIE_SECURE = True 
    CSRF_COOKIE_SECURE = True 
    SECURE_BROWSER_XSS_FILTER = True 
    SECURE_CONTENT_TYPE_NOSNIFF = True 
 
# Logging Configuration 
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO') 
LOGGING = { 
    'version': 1, 
    'disable_existing_loggers': False, 
    'formatters': { 
        'verbose': { 
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}', 
            'style': '{', 
        }, 
        'simple': { 
            'format': '{levelname} {message}', 
            'style': '{', 
        }, 
    }, 
    'handlers': { 
        'file': { 
            'level': LOG_LEVEL, 
            'class': 'logging.FileHandler', 
            'filename': os.path.join(BASE_DIR, os.getenv('LOG_FILE', 'debug.log')), 
            'formatter': 'verbose' 
        }, 
        'console': { 
            'level': 'DEBUG', 
            'class': 'logging.StreamHandler', 
            'formatter': 'simple' 
        }, 
    }, 
    'loggers': { 
        'django': { 
            'handlers': ['file', 'console'], 
            'level': LOG_LEVEL, 
            'propagate': True, 
        }, 
        'core': { 
            'handlers': ['file', 'console'], 
            'level': LOG_LEVEL, 
            'propagate': True, 
        }, 
    }, 
} 
