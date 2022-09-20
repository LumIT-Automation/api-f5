import os

import django
from django.conf import settings
from django.test import Client


####################################################################################################################
# A Test client stub
####################################################################################################################

# pip3 requirements:
#     (pip install --upgrade pip)
# Django~=3.2
# djangorestframework~=3.12.4
# requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
settings.DISABLE_AUTHENTICATION = True
settings.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'f5.db',
    }
}
settings.CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}
settings.REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': None,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '600/minute',
        'user': '600/minute'
    }
}
django.setup()

try:
    r = Client().get('/api/v1/f5/2/Partition1/nodes/').json()
    print(
        r["data"]["items"][0]
    )
except KeyError:
    pass
except Exception:
    print("Some error occurred.")

# Call:
# python -W ignore::Warning /var/www/api/test.client.py
