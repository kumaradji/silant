# settings.py
# Это файл настроек Django, определяющий конфигурацию для проекта silant

from pathlib import Path
import os

# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для криптографических подписей
SECRET_KEY = 'django-insecure-!8c280vpq9-e4xg%5c4g^7*20js18v)1*zy+-5p702&$^3jjmr'

# Включение отладки (True только для разработки)
DEBUG = True

# Адаптер для отключения регистрации пользователей через allauth
ACCOUNT_ADAPTER = 'inventory.adapters.NoSignupAccountAdapter'

# Список разрешённых хостов
ALLOWED_HOSTS = []

# Определение установленных приложений
INSTALLED_APPS = [
    'django.contrib.admin',  # Админка Django
    'django.contrib.auth',  # Аутентификация
    'django.contrib.contenttypes',  # Система типов контента
    'django.contrib.sessions',  # Сессии
    'django.contrib.messages',  # Сообщения
    'django.contrib.staticfiles',  # Статические файлы
    'django_filters',  # Фильтрация данных
    'inventory',  # Приложение inventory
]

# Настройки URL перенаправлений для входа и выхода
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Определение используемых промежуточных слоев (middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой URL конфигурации проекта
ROOT_URLCONF = 'silant.urls'

# Определение шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

# WSGI-приложение
WSGI_APPLICATION = 'silant.wsgi.application'

# Настройки базы данных (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Язык и временная зона
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'

# Настройки интернационализации
USE_I18N = True
USE_TZ = True

# Настройки для статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Настройка для автоматического поля первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
