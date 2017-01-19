#!/usr/bin/env python
import logging
import os
import sys

import django

BASE_PATH = os.path.dirname(__file__)

logging.basicConfig()


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app
    installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    sys.exc_clear()

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    # Override Settings
    global_settings.ROOT_URLCONF = "iss.tests.test_project.urls"

    # ISS  Settings:

    global_settings.MS_ACCESS_KEY = os.environ.get('MS_ACCESS_KEY', None)
    global_settings.MS_SECRET_KEY = os.environ.get('MS_SECRET_KEY', None)
    global_settings.MS_ASSOCIATION_ID = os.environ.get(
        'MS_ASSOCIATION_ID', None)
    global_settings.MS_USER_ID = os.environ.get('MS_USER_ID', None)
    global_settings.MS_USER_PASS = os.environ.get('MS_USER_PASS', None)

    global_settings.USE_TZ = True

    global_settings.STATIC_URL = '/static/'
    global_settings.STATIC_ROOT = ''

    global_settings.INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'iss',
        'membersuite-api-client'
    )

    if django.VERSION > (1, 2):
        global_settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_PATH, 'connpass.sqlite'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
    else:
        global_settings.DATABASE_ENGINE = "sqlite3"
        global_settings.DATABASE_NAME = ":memory:"

    global_settings.MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

    global_settings.SECRET_KEY = "blahblah"

    global_settings.SITE_ID = 1

    django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['iss'], fail_fast=True)
    else:
        failures = test_runner(['iss'], verbosity=1, fail_fast=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()
