# inventory/models.py

from django.db import models
from django.contrib.auth.models import User


class Machine(models.Model):
    serial_number = models.CharField(max_length=255, unique=True)
    model_technique = models.CharField(max_length=255)
    model_engine = models.CharField(max_length=255)
    serial_engine = models.CharField(max_length=255)
    model_transmission = models.CharField(max_length=255)
    serial_transmission = models.CharField(max_length=255)
    model_drive_axle = models.CharField(max_length=255)
    serial_drive_axle = models.CharField(max_length=255)
    model_steering_axle = models.CharField(max_length=255)
    serial_steering_axle = models.CharField(max_length=255)
    delivery_contract = models.CharField(max_length=255)
    shipment_date = models.DateField()
    customer = models.ForeignKey(User, related_name='customer_machines', on_delete=models.CASCADE)
    service_company = models.ForeignKey(User, related_name='service_machines', on_delete=models.CASCADE)

    def __str__(self):
        return self.serial_number


class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=255)
    maintenance_date = models.DateField()
    operating_time = models.PositiveIntegerField()
    order_number = models.CharField(max_length=255)
    order_date = models.DateField()
    service_company = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.machine} - {self.maintenance_type}'


class Reclamation(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    failure_date = models.DateField()
    operating_time = models.PositiveIntegerField()
    failure_unit = models.CharField(max_length=255)
    failure_description = models.TextField()
    recovery_method = models.CharField(max_length=255)
    used_spare_parts = models.TextField()
    recovery_date = models.DateField()
    downtime = models.PositiveIntegerField()
    service_company = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.machine} - {self.failure_unit}'
