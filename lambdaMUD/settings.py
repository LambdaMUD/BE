from decouple import config
import dj_database_url
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MIDDLEWARE = [
  # 'django.middleware.security.SecurityMiddleware',
  'whitenoise.middleware.WhiteNoiseMiddleware',
  # ...
]

DEBUG = config('DEBUG', cast = bool)

WSGI_APPLICATION = 'lambdaMUD.wsgi.application'

SECRET_KEY = config('SECRET_KEY')
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
ALLOWED_HOSTS = ['.herokuapp.com']
