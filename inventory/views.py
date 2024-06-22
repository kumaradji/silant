from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
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


def index_view(request):
    return render(request, 'inventory/index.html')


def machine_search_view(request):
    query = request.GET.get('serial_number')
    machine = Machine.objects.filter(serial_number=query).first()
    if machine:
        return render(request, 'inventory/machine_search_result.html', {'machine': machine})
    else:
        return render(request, 'inventory/machine_search_result.html',
                      {'error': 'Данных о машине с таким заводским номером нет в системе.'})


@login_required
def dashboard_view(request):
    user = request.user
    machines = Machine.objects.filter(owner=user)
    maintenances = Maintenance.objects.filter(machine__in=machines)
    reclamations = Reclamation.objects.filter(machine__in=machines)
    return render(request, 'inventory/dashboard.html', {
        'machines': machines,
        'maintenances': maintenances,
        'reclamations': reclamations
    })


@login_required
def machine_detail_view(request, id):
    machine = get_object_or_404(Machine, id=id)
    return render(request, 'inventory/machine_detail.html', {'machine': machine})


@login_required
def maintenance_detail_view(request, id):
    maintenance = get_object_or_404(Maintenance, id=id)
    return render(request, 'inventory/maintenance_detail.html', {'maintenance': maintenance})


@login_required
def reclamation_detail_view(request, id):
    reclamation = get_object_or_404(Reclamation, id=id)
    return render(request, 'inventory/reclamation_detail.html', {'reclamation': reclamation})
