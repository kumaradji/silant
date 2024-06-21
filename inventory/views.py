from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Machine, Maintenance, Reclamation


def is_client(user):
    return user.groups.filter(name='client').exists()


def is_service_company(user):
    return user.groups.filter(name='service_company').exists()


def is_manager(user):
    return user.groups.filter(name='manager').exists()


@login_required
@user_passes_test(is_client)
def client_view(request):
    machines = Machine.objects.filter(customer=request.user).order_by('shipment_date')
    maintenances = Maintenance.objects.filter(machine__customer=request.user).order_by('maintenance_date')
    reclamations = Reclamation.objects.filter(machine__customer=request.user).order_by('failure_date')
    return render(request, 'inventory/client_view.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
    })


@login_required
@user_passes_test(is_service_company)
def service_company_view(request):
    machines = Machine.objects.filter(service_company=request.user).order_by('shipment_date')
    maintenances = Maintenance.objects.filter(service_company=request.user).order_by('maintenance_date')
    reclamations = Reclamation.objects.filter(service_company=request.user).order_by('failure_date')
    return render(request, 'inventory/service_company_view.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
    })


@login_required
@user_passes_test(is_manager)
def manager_view(request):
    machines = Machine.objects.all().order_by('shipment_date')
    maintenances = Maintenance.objects.all().order_by('maintenance_date')
    reclamations = Reclamation.objects.all().order_by('failure_date')
    return render(request, 'inventory/manager_view.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
    })


def search_machine(request):
    serial_number = request.GET.get('serial_number')
    machines = Machine.objects.filter(serial_number=serial_number) if serial_number else None
    return render(request, 'inventory/search_machine.html', {'machines': machines})


@login_required
def machine_detail_view(request, machine_id):
    machine = Machine.objects.get(id=machine_id)
    return render(request, 'inventory/machine_detail.html', {'machine': machine})


@login_required
def main_view(request):
    user = request.user
    if user.groups.filter(name='client').exists():
        machines = Machine.objects.filter(customer=user).order_by('shipment_date')
        maintenances = Maintenance.objects.filter(machine__customer=user).order_by('maintenance_date')
        reclamations = Reclamation.objects.filter(machine__customer=user).order_by('failure_date')
    elif user.groups.filter(name='service_company').exists():
        machines = Machine.objects.filter(service_company=user).order_by('shipment_date')
        maintenances = Maintenance.objects.filter(service_company=user).order_by('maintenance_date')
        reclamations = Reclamation.objects.filter(service_company=user).order_by('failure_date')
    else:  # Manager or other roles
        machines = Machine.objects.all().order_by('shipment_date')
        maintenances = Maintenance.objects.all().order_by('maintenance_date')
        reclamations = Reclamation.objects.all().order_by('failure_date')

    return render(request, 'inventory/main.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
    })


def welcome_view(request):
    serial_number = request.GET.get('serial_number')
    machines = Machine.objects.filter(serial_number=serial_number) if serial_number else None
    return render(request, 'inventory/welcome.html', {'machines': machines})
