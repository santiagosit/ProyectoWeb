"""
Django settings for ProyectoWeb project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# settings.py

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--^!j0zutxz=)2th+qql@8&4%ko%)8p9ddcc^zia(u0-me$b%_1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['djangoelectronics.store','127.0.0.1','localhost']

CRSF_TRUSTED_ORIGINS = ['https://djangoelectronics.store/', 'https://127.0.0.1:8000', 'localhost']

# Application definition

INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_usuarios',
    'app_pedidos',
    'app_pagos',
    'app_reportes',
    'app_inventario',
    'app_finanzas',
    'app_ventas',
    'app_administracion',
    'app_eventos',
    'app_predicciones',
    'django_ses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ProyectoWeb.middleware.LoginRequiredMiddleware',
] 

ROOT_URLCONF = 'ProyectoWeb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': dict(context_processors=[
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
            'app_inventario.views.notificaciones',
            'app_usuarios.context_processors.add_profile_to_context',
        ]),
    },
]
WSGI_APPLICATION = 'ProyectoWeb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # MariaDB utiliza el motor MySQL en Django
        'NAME': 'proyecto_tienda',  # Nombre de la base de datos
        'USER': 'root',               # Usuario de MariaDB
        'PASSWORD': '0000',        # Contraseña de MariaDB
        'HOST': 'localhost',                # Dirección del servidor (local o remota)
        'PORT': '3306',                     # Puerto por defecto de MariaDB
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_ACCESS_KEY_ID = 'AKIASVLKB7LXKBF4W5X6'
AWS_SECRET_ACCESS_KEY = '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'
AWS_SES_REGION_NAME = 'us-east-1'  # Ajusta según tu región
AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'  # Ajusta

# Configuración de Login y Permisos
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Lista de URLs que no requieren autenticación
LOGIN_EXEMPT_URLS = [
    r'^$',
    r'^login/$',
    r'^recuperar/$',
    r'^verificar_pin/$',
    r'^reset_password/.*$',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

