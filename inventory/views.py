from datetime import datetime
import json
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
    if request.method == 'POST':
        data = json.loads(request.body)
        for item in data:
            machine = Machine.objects.get(id=item['id'])
            machine.model_technique = item['model_technique']
            machine.serial_number = item['serial_number']
            machine.model_engine = item['model_engine']
            machine.model_transmission = item['model_transmission']
            machine.model_drive_axle = item['model_drive_axle']
            machine.model_steering_axle = item['model_steering_axle']
            machine.shipment_date = item['shipment_date']
            machine.save()
        return JsonResponse({'status': 'success'})


@csrf_exempt
def save_maintenances(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for item in data:
                print(f"Processing item: {item}")  # Логирование полученного элемента
                maintenance = Maintenance.objects.get(id=item['id'])
                maintenance.maintenance_type = item['maintenance_type']
                try:
                    maintenance_date = datetime.strptime(item['maintenance_date'], '%Y-%m-%d').date()
                except ValueError as e:
                    print(f"Error parsing date for item {item}: {e}")
                    continue
                maintenance.maintenance_date = maintenance_date
                maintenance.operating_time = item['operating_time']
                maintenance.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(f"Unexpected error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)





@csrf_exempt
def save_reclamations(request):
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
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def is_client(user):
    return user.groups.filter(name='Клиент').exists()


def is_service_company(user):
    return user.groups.filter(name='Сервисная организация').exists()


def is_manager(user):
    return user.groups.filter(name='Менеджер').exists()


@login_required
@user_passes_test(is_client)
def client_view(request):
    machines = Machine.objects.filter(customer=request.user)
    maintenances = Maintenance.objects.filter(machine__customer=request.user)
    reclamations = Reclamation.objects.filter(machine__customer=request.user)

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
    machines = Machine.objects.filter(service_company=request.user)
    maintenances = Maintenance.objects.filter(machine__service_company=request.user)
    reclamations = Reclamation.objects.filter(machine__service_company=request.user)

    machine_filter = MachineFilter(request.GET, queryset=machines)
    maintenance_filter = MaintenanceFilter(request.GET, queryset=maintenances)
    reclamation_filter = ReclamationFilter(request.GET, queryset=reclamations)

    return render(request, 'inventory/service_company_view.html', {
        'machine_filter': machine_filter,
        'maintenance_filter': maintenance_filter,
        'reclamation_filter': reclamation_filter
    })


@login_required
@user_passes_test(is_manager)
def manager_view(request):
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
    machine = get_object_or_404(Machine, id=machine_id)
    return render(request, 'inventory/machine_detail.html', {'machine': machine})


@login_required
def maintenance_detail_view(request, maintenance_id):
    maintenance = get_object_or_404(Maintenance, id=maintenance_id)
    return render(request, 'inventory/maintenance_detail.html', {'maintenance': maintenance})


@login_required
def reclamation_detail_view(request, reclamation_id):
    reclamation = get_object_or_404(Reclamation, id=reclamation_id)
    return render(request, 'inventory/reclamation_detail.html', {'reclamation': reclamation})


@login_required
def main_view(request):
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
    serial_number = request.GET.get('serial_number')
    machines = []
    search_performed = False

    if serial_number:
        machines = Machine.objects.filter(serial_number=serial_number)
        search_performed = True

    all_machines = Machine.objects.all()[:10]  # Показать ограниченное количество машин для всех пользователей
    context = {
        'machines': machines,
        'all_machines': all_machines,
        'search_performed': search_performed,
    }
    return render(request, 'inventory/welcome.html', context)
