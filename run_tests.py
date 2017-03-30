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

    # ISS  Settings:

    global_settings.MS_ACCESS_KEY = os.environ.get('MS_ACCESS_KEY', None)
    global_settings.MS_SECRET_KEY = os.environ.get('MS_SECRET_KEY', None)
    global_settings.MS_ASSOCIATION_ID = os.environ.get(
        'MS_ASSOCIATION_ID', None)
    global_settings.MS_USER_ID = os.environ.get('MS_USER_ID', None)
    global_settings.MS_USER_PASS = os.environ.get('MS_USER_PASS', None)
    global_settings.INSTALLED_APPS = ('iss',)

    global_settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_PATH, 'iss.sqlite'),
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

    global_settings.SECRET_KEY = "blahblah"

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 7):
        django.setup()

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['iss'])
    else:
        failures = test_runner(['iss'], verbosity=2)

    sys.exit(failures)

if __name__ == '__main__':
    main()
