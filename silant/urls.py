# silant/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),  # Включает URL-ы приложения inventory
    path('accounts/', include('django.contrib.auth.urls')),  # Включает URL-ы для входа/выхода и т.д.
]