from django.db import models
from django.contrib.auth.models import User


class Machine(models.Model):
    serial_number = models.CharField(max_length=128, unique=True, verbose_name='Зав. № машины')
    model_technique = models.CharField(max_length=128, verbose_name='Модель техники')
    model_engine = models.CharField(max_length=128, verbose_name='Модель двигателя')
    serial_engine = models.CharField(max_length=128, verbose_name='Зав. № двигателя')
    model_transmission = models.CharField(max_length=128, verbose_name='Модель трансмиссии')
    serial_transmission = models.CharField(max_length=128, verbose_name='Зав. № трансмиссии')
    model_drive_axle = models.CharField(max_length=128, verbose_name='Модель ведущего моста')
    serial_drive_axle = models.CharField(max_length=128, verbose_name='Зав. № ведущего моста')
    model_steering_axle = models.CharField(max_length=128, verbose_name='Модель управляемого моста')
    serial_steering_axle = models.CharField(max_length=128, verbose_name='Зав. № управляемого моста')
    delivery_contract = models.CharField(max_length=128, verbose_name='Договор поставки')
    shipment_date = models.DateField(verbose_name='Дата отгрузки с завода')
    customer = models.ForeignKey(User, related_name='customer_machines', on_delete=models.CASCADE,
                                 verbose_name='Покупатель')
    consignee = models.ForeignKey(User, related_name='consignee_machines', on_delete=models.CASCADE,
                                  verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.CharField(max_length=128, verbose_name='Адрес поставки (эксплуатации)')
    configuration = models.TextField(verbose_name='Комплектация (доп. опции)')
    service_company = models.ForeignKey(User, related_name='service_machines', on_delete=models.CASCADE,
                                        verbose_name='Сервисная компания')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.serial_number

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        ordering = ['shipment_date']


class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='Зав. № машины')
    maintenance_type = models.CharField(max_length=128, verbose_name='Вид ТО')
    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')
    operating_time = models.PositiveIntegerField(verbose_name='Наработка, м/час')
    order_number = models.CharField(max_length=128, verbose_name='№ заказ-наряда')
    order_date = models.DateField(verbose_name='Дата заказ-наряда')
    service_company = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Организация, проводившая ТО')

    def __str__(self):
        return f'{self.machine} - {self.maintenance_type}'

    class Meta:
        verbose_name = 'Обслуживание'
        verbose_name_plural = 'Обслуживания'
        ordering = ['maintenance_date']


class Reclamation(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, verbose_name='Зав. № машины')
    failure_date = models.DateField(verbose_name='Дата отказа')
    operating_time = models.PositiveIntegerField(verbose_name='Наработка, м/час')
    failure_unit = models.CharField(max_length=128, verbose_name='Узел отказа')
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.CharField(max_length=128, verbose_name='Способ восстановления')
    used_spare_parts = models.TextField(verbose_name='Используемые запасные части')
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    downtime = models.PositiveIntegerField(verbose_name='Время простоя техники')
    service_company = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Сервисная компания')

    def __str__(self):
        return f'{self.machine} - {self.failure_unit}'

    def save(self, *args, **kwargs):
        # Calculate downtime before saving
        if self.failure_date and self.recovery_date:
            self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Рекламация'
        verbose_name_plural = 'Рекламации'
        ordering = ['failure_date']
