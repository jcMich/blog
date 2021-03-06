# Django settings for blog_system project.
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
PROJECT_PATH = os.path.dirname(os.path.dirname(__file__))

CRISPY_TEMPLATE_PACK = 'bootstrap3'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Chicago'

LANGUAGE_CODE = 'es-mx'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

USE_TZ = False


SECRET_KEY = 'mx-1t#-8()r*wnba1wo)s)%xim6a66d8y7w!no%g+k(o&amp;4)4*s'

#procesador de contexto
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "blog.context_processors.blog_context_processor",
    'django.core.context_processors.request',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'blog_system.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'blog_system.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'endless_pagination',
    'blog',
    'crispy_forms',
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.path.join(PROJECT_PATH, 'db.db'),                        # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

DEFAULT_CHARSET = 'utf-8'

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(PROJECT_PATH, 'colstatic')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'media'),
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

#Email Config
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'yezdotickets@gmail.com'
EMAIL_HOST_PASSWORD ='yezdotickets.com'
EMAIL_USE_TLS =True


#Dynamic meta tags
SITE_DESCRIPTION = 'Basic Blog by Deipi.com'
SITE_LOCALE = LANGUAGE_CODE
SITE_TYPE = 'News blog'
SITE_TITLE = 'Blog Dubalu'
SITE_URL = 'http://www.dubalu.com'
SITE_IMAGE ='http://www.deipi.com/static/images/html/deipi/deipi_logo.png?'
SITE_TWITTER = '@twitter'

# config

POSTS_ENTRIES_POST_ENTRY_MODEL = 'blog.BlogEntry'


# Defautl Views
BLOG_ENTRIES_HOME_VIEW = 'blog.views.home'
BLOG_ENTRIES_ENTRY_DETAIL_VIEW = 'blog.views.blog_entry_detail'
BLOG_ENTRIES_ENTRY_CREATE_VIEW = 'blog.views.create_blog_entry'
BLOG_ENTRIES_ENTRY_UPDATE_VIEW = 'blog.views.update_blog_entry'
BLOG_ENTRIES_CREATE_CATEGORY_VIEW = 'blog.views.create_category'
BLOG_ENTRIES_ENTRIES_ADMIN_VIEW = 'blog.views.admin_entries'
BLOG_ENTRIES_CATEGORIES_ADMIN_VIEW = 'blog.views.admin_categories'
BLOG_IMAGES_LIST = 'blog.views.images_list'

# Endles pagination
ENDLESS_PAGINATION_PREVIOUS_LABEL = "«"
ENDLESS_PAGINATION_NEXT_LABEL = "»"
