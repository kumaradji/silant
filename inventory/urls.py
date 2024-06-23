from django.urls import path
from .views import (
    welcome_view,
    client_view,
    service_company_view,
    manager_view,
    main_view,
    machine_detail_view,
    maintenance_detail_view,
    reclamation_detail_view,
    login_view
)

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('client_view/', client_view, name='client_view'),
    path('service_company_view/', service_company_view, name='service_company_view'),
    path('manager_view/', manager_view, name='manager_view'),
    path('main/', main_view, name='main'),
    path('machine/<int:machine_id>/', machine_detail_view, name='machine_detail'),
    path('maintenance/<int:maintenance_id>/', maintenance_detail_view, name='maintenance_detail'),
    path('reclamation/<int:reclamation_id>/', reclamation_detail_view, name='reclamation_detail'),
    path('login/', login_view, name='login'),
]
