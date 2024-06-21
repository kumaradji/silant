# inventory/urls.py

from django.urls import path
from .views import welcome_view, search_machine, client_view, service_company_view, manager_view, main_view, machine_detail_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('search_machine/', search_machine, name='search_machine'),
    path('client_view/', client_view, name='client_view'),
    path('service_company_view/', service_company_view, name='service_company_view'),
    path('manager_view/', manager_view, name='manager_view'),
    path('main/', main_view, name='main'),
    path('machine/<int:machine_id>/', machine_detail_view, name='machine_detail'),
]