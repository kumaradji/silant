import os
import django
import pandas as pd
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date
from inventory.models import Machine, Maintenance, Reclamation

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silant.settings')

# Initialize Django
django.setup()

# Path to your Excel file
excel_file_path = '/Users/kumar_air/WebstormProjects/silant/silant_bd.xlsx'

# Load data from Excel into a DataFrame
df = pd.read_excel(excel_file_path, sheet_name=None)  # Load all sheets from the file

# Data for the Machine model
machines_data = df['Машины']

for index, row in machines_data.iterrows():
    customer, _ = User.objects.get_or_create(username=row['Покупатель'])
    service_company, _ = User.objects.get_or_create(username=row['Сервисная компания'])

    machine = Machine.objects.create(
        serial_number=row['Зав. № машины'],
        model_technique=row['Модель техники'],
        model_engine=row['Модель двигателя'],
        serial_engine=row['Зав. № двигателя'],
        model_transmission=row['Модель трансмиссии'],
        serial_transmission=row['Зав. № трансмиссии'],
        model_drive_axle=row['Модель ведущего моста'],
        serial_drive_axle=row['Зав. № ведущего моста'],
        model_steering_axle=row['Модель управляемого моста'],
        serial_steering_axle=row['Зав. № управляемого моста'],
        delivery_contract=row['Грузополучатель'],
        shipment_date=parse_date(row['Дата отгрузки с завода']),
        customer=customer,
        service_company=service_company
    )

# Data for the Maintenance model
maintenance_data = df['Maintenance']

for index, row in maintenance_data.iterrows():
    service_company, _ = User.objects.get_or_create(username=row['Организация, проводившая ТО'])
    machine = Machine.objects.get(serial_number=row['Зав. № машины'])

    maintenance = Maintenance.objects.create(
        machine=machine,
        maintenance_type=row['Вид ТО'],
        maintenance_date=parse_date(row['Дата проведения ТО']),
        operating_time=int(row['Наработка, м/час']),
        order_number=row['№ заказ-наряда'],
        order_date=parse_date(row['дата заказ-наряда']),
        service_company=service_company
    )

# Data for the Reclamation model
reclamation_data = df['рекламация']

for index, row in reclamation_data.iterrows():
    service_company, _ = User.objects.get_or_create(username=row['Сервисная компания'])
    machine = Machine.objects.get(serial_number=row['Зав. № машины'])

    reclamation = Reclamation.objects.create(
        machine=machine,
        failure_date=parse_date(row['Дата отказа']),
        operating_time=int(row['Наработка, м/час']),
        failure_unit=row['Узел отказа'],
        failure_description=row['Описание отказа'],
        recovery_method=row['Способ восстановления'],
        used_spare_parts=row['Используемые запасные части'],
        recovery_date=parse_date(row['Дата восстановления']),
        downtime=int(row['Время простоя техники']),
        service_company=service_company
    )
