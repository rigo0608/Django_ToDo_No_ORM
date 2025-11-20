from pathlib import Path

# --------------------
#   BASE DIRECTORY
# --------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Root directory of the project

# --------------------
#   SECURITY
# --------------------
SECRET_KEY = 'replace-me-in-production'  # Change in production
DEBUG = True  # Turn off in production
ALLOWED_HOSTS = []  # Hosts allowed in production

# --------------------
#   INSTALLED APPS
# --------------------
INSTALLED_APPS = [
    'django.contrib.staticfiles',  # For serving static files
    'tasks',  # Our tasks app
]

# --------------------
#   MIDDLEWARE
# --------------------
MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',  # Common middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
]

# --------------------
#   URL CONFIG
# --------------------
ROOT_URLCONF = 'todo_project.urls'  # Main URL conf

# --------------------
#   TEMPLATES
# --------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Using Django templates
        'DIRS': [BASE_DIR / 'tasks' / 'templates'],  # Custom templates folder
        'APP_DIRS': True,
        'OPTIONS': {},  # Extra options can go here
    },
]

# --------------------
#   WSGI
# --------------------
WSGI_APPLICATION = 'todo_project.wsgi.application'  # WSGI entry point

# --------------------
#   STATIC FILES
# --------------------
STATIC_URL = '/static/'  # URL prefix for static files
STATICFILES_DIRS = [BASE_DIR / 'tasks' / 'static']  # Where static files live

# --------------------
#   DATABASE
# --------------------
# We are not using Django ORM; raw sqlite file used directly
# DB file path: BASE_DIR / 'db.sqlite3'
