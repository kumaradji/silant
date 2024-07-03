# silant/views.py
# Этот файл содержит определения представлений для обработки различных запросов и управления данными в приложении.

import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Machine, Maintenance, Reclamation
from .filters import MachineFilter, MaintenanceFilter, ReclamationFilter


@csrf_exempt
def save_machines(request):
    """
    Представление для сохранения данных о машинах.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                machine = Machine.objects.get(id=item['id'])
                machine.model_technique = item['model_technique']
                machine.serial_number = item['serial_number']
                machine.model_engine = item['model_engine']
                machine.model_transmission = item['model_transmission']
                machine.model_drive_axle = item['model_drive_axle']
                machine.model_steering_axle = item['model_steering_axle']
                machine.shipment_date = datetime.strptime(item['shipment_date'], '%Y-%m-%d').date()
                machine.save()
            return JsonResponse({'status': 'success'})
        except Machine.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Machine does not exist'}, status=400)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Unexpected error occurred'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def save_maintenances(request):
    """
    Представление для сохранения данных о техническом обслуживании.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                maintenance = Maintenance.objects.get(id=item['id'])
                maintenance.maintenance_type = item['maintenance_type']
                maintenance.maintenance_date = datetime.strptime(item['maintenance_date'], '%Y-%m-%d').date()
                maintenance.operating_time = item['operating_time']
                maintenance.save()
            return JsonResponse({'status': 'success'})
        except Maintenance.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Maintenance record does not exist'}, status=400)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Unexpected error occurred'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


@csrf_exempt
def save_reclamations(request):
    """
    Представление для сохранения данных о рекламациях.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                reclamation = Reclamation.objects.get(id=item['id'])
                reclamation.failure_date = datetime.strptime(item['failure_date'], '%Y-%m-%d').date()
                reclamation.operating_time = item['operating_time']
                reclamation.failure_unit = item['failure_unit']
                reclamation.recovery_method = item['recovery_method']
                reclamation.save()
            return JsonResponse({'status': 'success'})
        except Reclamation.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Reclamation does not exist'}, status=400)
        except ValueError as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Unexpected error occurred'}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def is_client(user):
    """
    Проверяет, является ли пользователь клиентом.
    """
    return user.groups.filter(name='Клиент').exists()


def is_service_company(user):
    """
    Проверяет, является ли пользователь представителем сервисной компании.
    """
    return user.groups.filter(name='Сервисная организация').exists()


def is_manager(user):
    """
    Проверяет, является ли пользователь менеджером.
    """
    return user.groups.filter(name='Менеджер').exists()


@login_required
@user_passes_test(is_client)
def client_view(request):
    """
    Представление для отображения данных для клиентов.
    """
    machines = Machine.objects.filter(customer=request.user) | Machine.objects.filter(consignee=request.user)
    maintenances = Maintenance.objects.filter(machine__customer=request.user) | Maintenance.objects.filter(
        machine__consignee=request.user)
    reclamations = Reclamation.objects.filter(machine__customer=request.user) | Reclamation.objects.filter(
        machine__consignee=request.user)

    machine_filter = MachineFilter(request.GET, queryset=machines)
    maintenance_filter = MaintenanceFilter(request.GET, queryset=maintenances)
    reclamation_filter = ReclamationFilter(request.GET, queryset=reclamations)

    return render(request, 'inventory/client_view.html', {
        'machine_filter': machine_filter,
        'maintenance_filter': maintenance_filter,
        'reclamation_filter': reclamation_filter
    })


@login_required
@user_passes_test(is_service_company)
def service_company_view(request):
    """
    Представление для отображения данных для сервисных компаний.
    """
    user = request.user
    machines = Machine.objects.filter(service_company=request.user)
    maintenances = Maintenance.objects.filter(machine__service_company=request.user)
    reclamations = Reclamation.objects.filter(machine__service_company=request.user)

    machine_filter = MachineFilter(request.GET, queryset=machines)
    maintenance_filter = MaintenanceFilter(request.GET, queryset=maintenances)
    reclamation_filter = ReclamationFilter(request.GET, queryset=reclamations)

    return render(request, 'inventory/service_company_view.html', {
        'user': user,
        'machine_filter': machine_filter,
        'maintenance_filter': maintenance_filter,
        'reclamation_filter': reclamation_filter
    })


@login_required
@user_passes_test(is_manager)
def manager_view(request):
    """
    Представление для отображения данных для менеджеров.
    """
    machines = Machine.objects.all()
    maintenances = Maintenance.objects.all()
    reclamations = Reclamation.objects.all()

    machine_filter = MachineFilter(request.GET, queryset=machines)
    maintenance_filter = MaintenanceFilter(request.GET, queryset=maintenances)
    reclamation_filter = ReclamationFilter(request.GET, queryset=reclamations)

    return render(request, 'inventory/manager_view.html', {
        'machine_filter': machine_filter,
        'maintenance_filter': maintenance_filter,
        'reclamation_filter': reclamation_filter
    })


def login_view(request):
    """
    Представление для входа в систему.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.groups.filter(name='Клиент').exists():
                return redirect('client_view')
            elif user.groups.filter(name='Сервисная организация').exists():
                return redirect('service_company_view')
            elif user.groups.filter(name='Менеджер').exists():
                return redirect('manager_view')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def machine_detail_view(request, machine_id):
    """
    Представление для отображения детальной информации о машине.
    """
    machine = get_object_or_404(Machine, id=machine_id)
    return render(request, 'inventory/machine_detail.html', {'machine': machine})


@login_required
def main_view(request):
    """
    Представление для отображения главной страницы в зависимости от роли пользователя.
    """
    user = request.user

    machine_filter = MachineFilter(request.GET, queryset=Machine.objects.all())
    maintenance_filter = MaintenanceFilter(request.GET, queryset=Maintenance.objects.all())
    reclamation_filter = ReclamationFilter(request.GET, queryset=Reclamation.objects.all())

    if user.groups.filter(name='Клиент').exists():
        machine_filter = MachineFilter(request.GET, queryset=Machine.objects.filter(customer=user))
        maintenance_filter = MaintenanceFilter(request.GET, queryset=Maintenance.objects.filter(machine__customer=user))
        reclamation_filter = ReclamationFilter(request.GET, queryset=Reclamation.objects.filter(machine__customer=user))
    elif user.groups.filter(name='Сервисная организация').exists():
        machine_filter = MachineFilter(request.GET, queryset=Machine.objects.filter(service_company=user))
        maintenance_filter = MaintenanceFilter(request.GET, queryset=Maintenance.objects.filter(service_company=user))
        reclamation_filter = ReclamationFilter(request.GET, queryset=Reclamation.objects.filter(service_company=user))

    return render(request, 'inventory/main.html', {
        'machine_filter': machine_filter,
        'maintenance_filter': maintenance_filter,
        'reclamation_filter': reclamation_filter,
    })


def welcome_view(request):
    """
    Представление для отображения главной страницы.
    """
    serial_number = request.GET.get('serial_number')
    machines = []
    search_performed = False

    if (serial_number):
        machines = Machine.objects.filter(serial_number=serial_number)
        search_performed = True

    all_machines = Machine.objects.all()[:10]  # Показать ограниченное количество машин для всех пользователей
    context = {
        'machines': machines,
        'all_machines': all_machines,
        'search_performed': search_performed,
    }
    return render(request, 'inventory/welcome.html', context)
