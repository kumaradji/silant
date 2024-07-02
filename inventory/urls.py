# silant/urls.py
# Этот файл содержит определения URL маршрутов для приложения, связывая URL с соответствующими представлениями.

from django.urls import path
from .views import (
    welcome_view,
    client_view,
    service_company_view,
    manager_view,
    machine_detail_view,
    save_machines,
    save_maintenances,
    save_reclamations,
    login_view
)

# Определение маршрутов URL и связывание их с соответствующими представлениями
urlpatterns = [
    path('', welcome_view, name='welcome'),  # Главная страница
    path('client_view/', client_view, name='client_view'),  # Страница клиента
    path('service_company_view/', service_company_view, name='service_company_view'),  # Страница сервисной компании
    path('manager_view/', manager_view, name='manager_view'),  # Страница менеджера
    path('machine/<int:machine_id>/', machine_detail_view, name='machine_detail'),  # Детальная информация о машине
    path('login/', login_view, name='login'),  # Страница входа в систему
    path('save_machines/', save_machines, name='save_machines'),  # Сохранение изменений в машинах
    path('save_maintenances/', save_maintenances, name='save_maintenances'),  # Сохранение изменений в ТО
    path('save_reclamations/', save_reclamations, name='save_reclamations'),  # Сохранение изменений в рекламациях
]
