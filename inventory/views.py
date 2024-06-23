from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Machine, Maintenance, Reclamation
from .filters import MachineFilter, MaintenanceFilter, ReclamationFilter


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
    return render(request, 'inventory/client_view.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
    })


@login_required
@user_passes_test(is_service_company)
def service_company_view(request):
    machines = Machine.objects.filter(service_company=request.user)
    maintenances = Maintenance.objects.filter(machine__service_company=request.user)
    reclamations = Reclamation.objects.filter(machine__service_company=request.user)
    return render(request, 'inventory/service_company_view.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
    })


@login_required
@user_passes_test(is_manager)
def manager_view(request):
    machines = Machine.objects.all()
    maintenances = Maintenance.objects.all()
    reclamations = Reclamation.objects.all()
    return render(request, 'inventory/manager_view.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
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
    machines = Machine.objects.filter(serial_number=serial_number) if serial_number else None
    return render(request, 'inventory/welcome.html', {'machines': machines})
