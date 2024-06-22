import django_tables2 as tables
from .models import Machine, Maintenance, Reclamation


class MachineTable(tables.Table):
    class Meta:
        model = Machine
        template_name = "django_tables2/bootstrap.html"
        fields = ("serial_number", "model_technique", "model_engine", "model_transmission", "model_drive_axle",
                  "model_steering_axle", "shipment_date")
        attrs = {'class': 'table'}


class MaintenanceTable(tables.Table):
    class Meta:
        model = Maintenance
        template_name = "django_tables2/bootstrap.html"
        fields = ("machine__serial_number", "maintenance_type", "maintenance_date", "service_company")
        attrs = {'class': 'table'}


class ReclamationTable(tables.Table):
    class Meta:
        model = Reclamation
        template_name = "django_tables2/bootstrap.html"
        fields = ("machine__serial_number", "failure_date", "failure_unit", "service_company")
        attrs = {'class': 'table'}
