from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib.auth.models import User

# Load environment variables from .env file
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".env"))


# Quick-start development settings - unsuitable for production
SECRET_KEY = str(os.getenv('SECRET_KEY'))
DEBUG = False if os.getenv('DJANGO_ENV') == 'production' else True

ALLOWED_HOSTS = ["virtulearn.vercel.app", ".vercel.app", "virtulearn-api.onrender.com", ".onrender.com", "127.0.0.1", "localhost"]


# Application definition
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
   "https://virtulearn.vercel.app",
]
CORS_ALLOW_CREDENTIALS = True



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'storages',

    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'rest_framework.authtoken',

    'base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # 'sonips_lms_backend.restrict_host_middleware.RestrictHostMiddleware',
]

ROOT_URLCONF = 'sonips_lms_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'sonips_lms_backend.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE':
    'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}



# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production Database
if os.environ.get('DJANGO_ENV') == 'production':
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.getenv('DB_NAME')) ,
        'USER': str(os.getenv('DB_USER')),
        'PASSWORD': str(os.getenv('DB_PASSWORD')),
        'HOST': str(os.getenv('DB_HOST')),
        'PORT': str(os.getenv('DB_PORT')),
        'OPTIONS': {'sslmode': 'require'},
    }


# Read environment variables
CREATE_SUPERUSER = os.getenv('CREATE_SUPERUSER', 'False').lower() == 'true'
DJANGO_SUPERUSER_EMAIL = os.getenv('DJANGO_SUPERUSER_EMAIL')
DJANGO_SUPERUSER_PASSWORD = os.getenv('DJANGO_SUPERUSER_PASSWORD')
DJANGO_SUPERUSER_USERNAME = os.getenv('DJANGO_SUPERUSER_USERNAME')

# Create superuser if enabled and necessary details are provided
if CREATE_SUPERUSER and DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD and DJANGO_SUPERUSER_USERNAME:
    if not User.objects.filter(username=DJANGO_SUPERUSER_USERNAME).exists():
        User.objects.create_superuser(DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, DJANGO_SUPERUSER_PASSWORD)
        print('Superuser created successfully.')
    else:
        print('Superuser already exists.')


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# AWS settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')

AWS_QUERYSTRING_AUTH = False 
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

AWS_LOCATION = 'static'
STATIC_LOCATION = 'static'
STATICFILES_LOCATION = 'staticfiles'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
STATIC_ROOT = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATICFILES_LOCATION}/'



# CSRF_COOKIE_SECURE and SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


# Server Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_REDIRECT_EXEMPT = []

# Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", "data:")
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_SRC = ("'self'",)
CSP_OBJECT_SRC = ("'none'",)
CSP_MEDIA_SRC = ("'self'",)
CSP_SANDBOX = ("allow-forms", "allow-scripts")


# Rate Limiting
REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = (
    'rest_framework.throttling.AnonRateThrottle',
    'rest_framework.throttling.UserRateThrottle',
)
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100/day',
    'user': '1000/day',
}

# Database Connection Pooling
DATABASES['default']['CONN_MAX_AGE'] = 600

# Automated Testing
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
NOSE_ARGS = [
    '--nocapture',
    '--nologcapture',
    '--with-id',
    '--with-yanc',
    '--failed',
    '--stop',
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


# ADMINS and MANAGERS
ADMINS = [('Precious Imoniakemu', 'preciousimoniakemu@gmail.com')]
MANAGERS = ADMINS


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL - SMTP SERVER
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.privateemail.com'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = False
# EMAIL_USE_SSL = True
# DEFAULT_FROM_EMAIL = 'Learn Online <info@sonipstechmart.com>'

CSRF_TRUSTED_ORIGINS = ['https://virtulearn-api.onrender.com','https://virtulearn.vercel.app']