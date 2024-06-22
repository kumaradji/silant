# silant/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView  # Импортируем LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # URL-ы приложения inventory
    path('accounts/', include('django.contrib.auth.urls')),  # URL-ы для входа/выхода и других функций аутентификации
    path('logout/', LogoutView.as_view(next_page='welcome'), name='logout'),  # Пример перенаправления на 'welcome'
]
