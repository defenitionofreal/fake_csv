import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-^-=a&k^q4^x_05kiv1nuj)nmmc9pl4df62s05o@3w(w1y-%38u'

DEBUG = False

ALLOWED_HOSTS = ['fakecsvgen.herokuapp.com', '127.0.0.1', 'localhost']

# Celery Configuration Options
CELERY_TIMEZONE = "Europe/Moscow"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_RESULT_BACKEND = 'django-db'  # shows ready status
CELERY_BROKER_URL = os.environ.get("REDISCLOUD_URL", "redis://") # work
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

#CELERY_BROKER_URL = 'redis://localhost:6379/0'  # for local
#CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = os.environ['REDIS_URL']   # didnt work. why?
# CELERY_RESULT_BACKEND = os.environ['REDIS_URL'] # didnt work. why?
# CELERY_BROKER_URL = 'redis://:p59c7ea534c4a1790f30dd9c816421fa8bd68ed883090a745e706037781520828@ec2-54-76-185-199.eu-west-1.compute.amazonaws.com:32310'   # didnt work. why?
# CELERY_RESULT_BACKEND = 'redis://:p59c7ea534c4a1790f30dd9c816421fa8bd68ed883090a745e706037781520828@ec2-54-76-185-199.eu-west-1.compute.amazonaws.com:32310'   # didnt work. why?
#CELERY_RESULT_BACKEND = os.environ.get("REDISCLOUD_URL", "redis://") # dont show status ready

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local
    'users',
    'csv_gen',
    # 3rd party
    'django_bootstrap5',
    "crispy_forms",
    "crispy_bootstrap5",
    'django_celery_results',
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

ROOT_URLCONF = 'csv_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'csv_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd53ailjq577tga',
        'HOST': 'ec2-34-254-69-72.eu-west-1.compute.amazonaws.com',
        'POST': 5432,
        'USER': 'ucnzruewiysefe',
        'PASSWORD': 'fe3f8e4e93e28bdc0169a23649200a27698910da498a6c1e0e262297838b199b',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
#STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

AUTH_USER_MODEL = 'users.CustomUser'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

