# inventory/filters.py

import django_filters
from .models import Machine, Maintenance, Reclamation


class MachineFilter(django_filters.FilterSet):
    model_technique = django_filters.CharFilter(field_name='model_technique', lookup_expr='icontains')
    model_engine = django_filters.CharFilter(field_name='model_engine', lookup_expr='icontains')
    model_transmission = django_filters.CharFilter(field_name='model_transmission', lookup_expr='icontains')
    model_drive_axle = django_filters.CharFilter(field_name='model_drive_axle', lookup_expr='icontains')
    model_steering_axle = django_filters.CharFilter(field_name='model_steering_axle', lookup_expr='icontains')

    class Meta:
        model = Machine
        fields = ['model_technique', 'model_engine', 'model_transmission', 'model_drive_axle', 'model_steering_axle']


class MaintenanceFilter(django_filters.FilterSet):
    maintenance_type = django_filters.CharFilter(field_name='maintenance_type', lookup_expr='icontains')
    serial_number = django_filters.CharFilter(field_name='machine__serial_number', lookup_expr='icontains')
    service_company = django_filters.CharFilter(field_name='service_company__username', lookup_expr='icontains')

    class Meta:
        model = Maintenance
        fields = ['maintenance_type', 'machine__serial_number', 'service_company']


class ReclamationFilter(django_filters.FilterSet):
    failure_unit = django_filters.CharFilter(field_name='failure_unit', lookup_expr='icontains')
    recovery_method = django_filters.CharFilter(field_name='recovery_method', lookup_expr='icontains')
    service_company = django_filters.CharFilter(field_name='service_company__username', lookup_expr='icontains')

    class Meta:
        model = Reclamation
        fields = ['failure_unit', 'recovery_method', 'service_company']
