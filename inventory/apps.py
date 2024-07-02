# silant/apps.py
# Этот файл определяет конфигурацию приложения Django для приложения Inventory.

from django.apps import AppConfig


class InventoryConfig(AppConfig):
    """
    Класс конфигурации приложения Inventory.
    Определяет имя приложения и значение по умолчанию для поля 'id' моделей.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inventory'
