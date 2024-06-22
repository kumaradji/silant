from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Machine, Maintenance, Reclamation


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


def search_machine(request):
    serial_number = request.GET.get('serial_number')
    machines = Machine.objects.filter(serial_number=serial_number) if serial_number else None
    return render(request, 'inventory/search_machine.html', {'machines': machines})


@login_required
def machine_detail_view(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    return render(request, 'inventory/machine_detail.html', {'machine': machine})


@login_required
def main_view(request):
    user = request.user
    if user.groups.filter(name='Клиент').exists():
        machines = Machine.objects.filter(customer=user).order_by('shipment_date')
        maintenances = Maintenance.objects.filter(machine__customer=user).order_by('maintenance_date')
        reclamations = Reclamation.objects.filter(machine__customer=user).order_by('failure_date')
    elif user.groups.filter(name='Сервисная организация').exists():
        machines = Machine.objects.filter(service_company=user).order_by('shipment_date')
        maintenances = Maintenance.objects.filter(service_company=user).order_by('maintenance_date')
        reclamations = Reclamation.objects.filter(service_company=user).order_by('failure_date')
    else:
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


@login_required
def dashboard_view(request):
    user = request.user

    model_technique = request.GET.get('model_technique')
    model_engine = request.GET.get('model_engine')
    model_transmission = request.GET.get('model_transmission')

    machines = Machine.objects.all()
    if model_technique:
        machines = machines.filter(model_technique=model_technique)
    if model_engine:
        machines = machines.filter(model_engine=model_engine)
    if model_transmission:
        machines = machines.filter(model_transmission=model_transmission)

    if user.groups.filter(name='Клиент').exists():
        machines = machines.filter(customer=user)
    elif user.groups.filter(name='Сервисная организация').exists():
        machines = machines.filter(service_company=user)

    context = {
        'user': user,
        'machines': machines,
        'maintenances': Maintenance.objects.filter(machine__in=machines),
        'reclamations': Reclamation.objects.filter(machine__in=machines),
        'model_techniques': Machine.objects.values_list('model_technique', flat=True).distinct(),
        'model_engines': Machine.objects.values_list('model_engine', flat=True).distinct(),
        'model_transmissions': Machine.objects.values_list('model_transmission', flat=True).distinct(),
    }

    return render(request, 'inventory/dashboard.html', context)


@login_required
def maintenance_detail_view(request, id):
    maintenance = get_object_or_404(Maintenance, id=id)
    return render(request, 'inventory/maintenance_detail.html', {'maintenance': maintenance})


@login_required
def reclamation_detail_view(request, id):
    reclamation = get_object_or_404(Reclamation, id=id)
    return render(request, 'inventory/reclamation_detail.html', {'reclamation': reclamation})
