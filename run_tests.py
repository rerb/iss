#!/usr/bin/env python
import logging
import os
import sys

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

    import django.test.utils

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"

    from django.conf import global_settings

    # ISS  Settings:

    global_settings.MS_ACCESS_KEY = os.environ["MS_ACCESS_KEY"]
    global_settings.MS_SECRET_KEY = os.environ["MS_SECRET_KEY"]
    global_settings.MS_ASSOCIATION_ID = os.environ["MS_ASSOCIATION_ID"]
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

    if django.VERSION > (1, 7):
        django.setup()

    test_runner = django.test.utils.get_runner(global_settings)

    if django.VERSION > (1, 2):
        failures = test_runner().run_tests(['iss'])

    else:
        failures = test_runner(['iss'], verbosity=2)

    sys.exit(failures)


if __name__ == '__main__':
    main()
