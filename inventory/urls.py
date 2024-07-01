from django.urls import path
from .views import (
    welcome_view,
    client_view,
    service_company_view,
    manager_view,
    main_view,
    machine_detail_view,
    save_machines,
    save_maintenances,
    save_reclamations,
    login_view
)

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('client_view/', client_view, name='client_view'),
    path('service_company_view/', service_company_view, name='service_company_view'),
    path('manager_view/', manager_view, name='manager_view'),
    path('main/', main_view, name='main'),
    path('machine/<int:machine_id>/', machine_detail_view, name='machine_detail'),
    path('login/', login_view, name='login'),
    path('save_machines/', save_machines, name='save_machines'),
    path('save_maintenances/', save_maintenances, name='save_maintenances'),
    path('save_reclamations/', save_reclamations, name='save_reclamations'),
]
