"""
Django settings for apimonitor project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'syf(by#w(+c#yne&n1460r0rue)k*_v5z84ynh3ueg&n88)c83'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'syf(by#w(+c#yne&n1460r0rue)k*_v5z84ynh3ueg&n88)c83')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
DEBUG = bool( os.environ.get('DJANGO_DEBUG', True))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'twitter_monitor',
    'rest_framework',
    'chartit',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)

ROOT_URLCONF = 'app_monit.urls'

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

WSGI_APPLICATION = 'app_monit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
  'NAME': 'd20anm1kpb1g24',
	'USER': 'rqenthqjldarpv',
	'HOST':'ec2-107-20-255-96.compute-1.amazonaws.com',
	'PORT':'5432',
	'PASSWORD':'7d07438ac5204ff1ee13e025c4ccc995b170690a98253ade96513a7b271b9a20',

 

 #uncomment to run  locally
	# 'NAME': 'mydb',
    # 'USER': 'myuser',
    # 'PASSWORD': '12345678',
    # 'HOST': '127.0.0.1',
    # 'PORT': '', # 8000 is default

}
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

LOGIN_REDIRECT_URL = '/monitoramentos'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

REST_FRAMEWORK = {
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
	'rest_framework.authentication.BasicAuthentication',
	'rest_framework.authentication.SessionAuthentication',
	'rest_framework.authentication.TokenAuthentication',
    )
}

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

#STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
