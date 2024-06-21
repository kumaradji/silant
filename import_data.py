import openpyxl
from django.contrib.auth.models import User

from inventory.models import Machine


def import_excel_data(file_path, model):
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if model == Machine:
            Machine.objects.create(
                serial_number=row[0],
                model_technique=row[1],
                model_engine=row[2],
                serial_engine=row[3],
                model_transmission=row[4],
                serial_transmission=row[5],
                model_drive_axle=row[6],
                serial_drive_axle=row[7],
                model_steering_axle=row[8],
                serial_steering_axle=row[9],
                delivery_contract=row[10],
                shipment_date=row[11],
                customer=User.objects.get(username=row[12]),
                service_company=User.objects.get(username=row[13])
            )
        elif model == Maintenance:
            Maintenance.objects.create(
                machine=Machine.objects.get(serial_number=row[0]),
                maintenance_type=row[1],
                maintenance_date=row[2],
                operating_time=row[3],
                order_number=row[4],
                order_date=row[5],
                service_company=User.objects.get(username=row[6])
            )
        elif model == Reclamation:
            Reclamation.objects.create(
                machine=Machine.objects.get(serial_number=row[0]),
                failure_date=row[1],
                operating_time=row[2],
                failure_unit=row[3],
                failure_description=row[4],
                recovery_method=row[5],
                used_spare_parts=row[6],
                recovery_date=row[7],
                downtime=row[8],
                service_company=User.objects.get(username=row[9])
            )


# Вызов функции для каждой таблицы
import_excel_data('/Users/kumar_air/WebstormProjects/silant/machines.xlsx', Machine)
import_excel_data('/Users/kumar_air/WebstormProjects/silant/maintenance.xlsx', Maintenance)
import_excel_data('/Users/kumar_air/WebstormProjects/silant/reclamations.xlsx', Reclamation)