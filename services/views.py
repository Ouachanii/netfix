
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from .models import Service, ServiceRequest, SERVICE_FIELD_CHOICES
from .forms import CreateNewService, RequestServiceForm
from users.models import Company

def service_list(request):
    services = Service.objects.all().order_by('-date')
    return render(request, 'services/list.html', {'services': services})

def index(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'services/single_service.html', {'service': service})

@login_required
def create(request):
    if not getattr(request.user, 'is_company', False):
        return redirect('/register/login/')
    company = request.user.company_profile
    form = CreateNewService(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        field = form.cleaned_data['field']
        # Restrict: company can create only in its field unless All in One
        if company.field_of_work != 'All in One' and company.field_of_work != field:
            form.add_error('field', 'Your company can only create services in its own field.')
        else:
            Service.objects.create(
                company=company,
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price_hour=form.cleaned_data['price_hour'],
                field=field
            )
            return redirect('/services/')
    return render(request, 'services/create.html', {'form': form})

def service_field(request, field):
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(field=field).order_by('-date')
    return render(request, 'services/field.html', {'services': services, 'field': field})

@login_required
def request_service(request, id):
    service = get_object_or_404(Service, id=id)
    if not getattr(request.user, 'is_customer', False):
        return redirect('/register/login/')
    form = RequestServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        sr = ServiceRequest.objects.create(
            service=service,
            customer=request.user.customer_profile,
            company=service.company,
            address=form.cleaned_data['address'],
            hours=form.cleaned_data['hours']
        )
        return redirect('/customer/{}'.format(request.user.username))
    return render(request, 'services/request_service.html', {'service': service, 'form': form})

def most_requested(request):
    services = Service.objects.annotate(req_count=Count('requests')).order_by('-req_count','-date')[:20]
    return render(request, 'services/most.html', {'services': services})
