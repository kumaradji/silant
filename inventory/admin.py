from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Machine, Maintenance, Reclamation


class MachineAdminForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MachineAdminForm, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = User.objects.all()
        self.fields['consignee'].queryset = User.objects.all()


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineAdminForm
    list_display = ('serial_number', 'model_technique', 'model_engine', 'customer', 'consignee', 'service_company')
    search_fields = ('serial_number', 'model_technique', 'model_engine')
    list_filter = ('model_technique', 'model_engine', 'customer', 'service_company')


@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type', 'maintenance_date', 'service_company')
    search_fields = ('machine__serial_number', 'maintenance_type')
    list_filter = ('maintenance_date', 'service_company')


@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('machine', 'failure_unit', 'failure_date', 'service_company')
    search_fields = ('machine__serial_number', 'failure_unit')
    list_filter = ('failure_date', 'service_company')
