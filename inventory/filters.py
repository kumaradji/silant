# silant/filters.py
# Этот файл содержит определение фильтров для моделей Machine, Maintenance и Reclamation, используемых в приложении.

import django_filters
from .models import Machine, Maintenance, Reclamation

class MachineFilter(django_filters.FilterSet):
    """
    Фильтр для модели Machine.
    Позволяет фильтровать данные о машинах по нескольким полям с помощью частичного совпадения (icontains).
    """
    model_technique = django_filters.CharFilter(
        field_name='model_technique',
        lookup_expr='icontains',
        label='Модель техники содержит'
    )
    model_engine = django_filters.CharFilter(
        field_name='model_engine',
        lookup_expr='icontains',
        label='Модель двигателя содержит'
    )
    model_transmission = django_filters.CharFilter(
        field_name='model_transmission',
        lookup_expr='icontains',
        label='Модель трансмиссии содержит'
    )
    model_steering_axle = django_filters.CharFilter(
        field_name='model_steering_axle',
        lookup_expr='icontains',
        label='Модель управляемого моста содержит'
    )
    model_drive_axle = django_filters.CharFilter(
        field_name='model_drive_axle',
        lookup_expr='icontains',
        label='Модель ведущего моста содержит'
    )

    class Meta:
        model = Machine
        fields = [
            'model_technique',
            'model_engine',
            'model_transmission',
            'model_steering_axle',
            'model_drive_axle'
        ]

class MaintenanceFilter(django_filters.FilterSet):
    """
    Фильтр для модели Maintenance.
    Позволяет фильтровать данные о техническом обслуживании по нескольким полям с помощью частичного совпадения (icontains).
    """
    maintenance_type = django_filters.CharFilter(
        field_name='maintenance_type',
        lookup_expr='icontains',
        label='Вид ТО содержит'
    )
    serial_number = django_filters.CharFilter(
        field_name='machine__serial_number',
        lookup_expr='icontains',
        label='Зав. № машины содержит'
    )
    service_company = django_filters.CharFilter(
        field_name='service_company__first_name',
        lookup_expr='icontains',
        label='Организация, проводившая ТО содержит'
    )

    class Meta:
        model = Maintenance
        fields = [
            'maintenance_type',
            'serial_number',
            'service_company'
        ]

class ReclamationFilter(django_filters.FilterSet):
    """
    Фильтр для модели Reclamation.
    Позволяет фильтровать данные о рекламациях по нескольким полям с помощью частичного совпадения (icontains).
    """
    failure_unit = django_filters.CharFilter(
        field_name='failure_unit',
        lookup_expr='icontains',
        label='Узел отказа содержит'
    )
    recovery_method = django_filters.CharFilter(
        field_name='recovery_method',
        lookup_expr='icontains',
        label='Способ восстановления содержит'
    )
    service_company = django_filters.CharFilter(
        field_name='service_company__first_name',
        lookup_expr='icontains',
        label='Сервисная компания содержит'
    )

    class Meta:
        model = Reclamation
        fields = [
            'failure_unit',
            'recovery_method',
            'service_company'
        ]
