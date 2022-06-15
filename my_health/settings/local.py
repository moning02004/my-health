from my_health.settings import BASE_DIR

SECRET_KEY = 'django-insecure-&2*v@=5d7dvz+53*a%tr)%53zf4z(f&5=02(%jjqxusz8jp6x='

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
