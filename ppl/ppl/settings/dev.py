from .base import *
from .secret import *
import sys

print(BASE_DIR)
"""
This section explains all the changes i make in this file
"""

"""
- Adding Postgresql db:
    - requires installing psycopg2
        - conda install -c anaconda psycopg2
    - adding it to installed apps
    - setting database info
"""
INSTALLED_APPS += ['psycopg2']

DATABASES = {
    'default':
    {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': POSTGRESS_DB,
        'USER': 'postgres',
        'PASSWORD': POSTGRESQL_PASS,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

"""
- Settings to allow django to find the `templates` and `static` folders.
"""
# Templates
TEMPLATES[0]['DIRS'] = [
    os.path.join(BASE_DIR, 'templates'),
]

# Static
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

"""
- Adding support for 'apps' folder usage.
"""
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

"""
- Created a 'mdb' app, now adding it to settings.
"""

INSTALLED_APPS += ['mdb.apps.MdbConfig']