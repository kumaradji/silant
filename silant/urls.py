# silant/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from inventory import views
from django.conf import settings
from django.conf.urls.static import static

"""
Конфигурация URL

Список `urlpatterns` направляет URL-адреса на представления. 
Для получения дополнительной информации, пожалуйста, посетите:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/

Примеры:
Функции представлений
    1. Добавьте импорт:  from my_app import views
    2. Добавьте URL в urlpatterns:  path('', views.home, name='home')

Представления на основе классов
    1. Добавьте импорт:  from other_app.views import Home
    2. Добавьте URL в urlpatterns:  path('', Home.as_view(), name='home')

Включение другого URLconf
    1. Импортируйте функцию include(): from django.urls import include, path
    2. Добавьте URL в urlpatterns:  path('blog/', include('blog.urls'))
"""

# URL-шаблоны для приложения
urlpatterns = [
    # Админ-панель
    path('admin/', admin.site.urls),

    # Включение URL из приложения inventory
    path('', include('inventory.urls')),

    # Пользовательская страница входа
    path('accounts/login/', views.login_view, name='login'),

    # Встроенные URL аутентификации Django
    path('accounts/', include('django.contrib.auth.urls')),

    # Пользовательская страница выхода с перенаправлением на страницу приветствия
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Конфигурация статических файлов
