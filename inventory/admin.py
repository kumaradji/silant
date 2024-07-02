# silant/admin.py
# Этот файл определяет формы и админские представления для моделей Machine, Maintenance и Reclamation.
# Эти представления используются в Django Admin для управления данными этих моделей.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Machine, Maintenance, Reclamation


class MachineAdminForm(forms.ModelForm):
    """
    Форма для модели Machine в админке. Определяет все поля модели и
    настраивает queryset для полей customer, consignee и service_company,
    чтобы они включали всех пользователей.
    """

    class Meta:
        model = Machine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MachineAdminForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = User.objects.all()
        self.fields['consignee'].queryset = User.objects.all()
        self.fields['service_company'].queryset = User.objects.all()


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    """
    Админское представление для модели Machine.
    Определяет отображаемые поля в списке, поля для поиска и фильтры.
    """
    form = MachineAdminForm
    list_display = ('serial_number', 'model_technique', 'model_engine', 'customer', 'consignee', 'service_company')
    search_fields = ('serial_number', 'model_technique', 'model_engine')
    list_filter = ('model_technique', 'model_engine', 'customer', 'service_company')


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    """
    Админское представление для модели Maintenance.
    Определяет отображаемые поля в списке, поля для поиска и фильтры.
    """
    list_display = ('machine', 'maintenance_type', 'maintenance_date', 'service_company')
    search_fields = ('machine__serial_number', 'maintenance_type')
    list_filter = ('maintenance_date', 'service_company')


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    """
    Админское представление для модели Reclamation.
    Определяет отображаемые поля в списке, поля для поиска и фильтры.
    """
    list_display = ('machine', 'failure_unit', 'failure_date', 'service_company')
    search_fields = ('machine__serial_number', 'failure_unit')
    list_filter = ('failure_date', 'service_company')
