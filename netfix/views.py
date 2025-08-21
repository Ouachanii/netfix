
from django.shortcuts import render, get_object_or_404
from datetime import date

from users.models import User, Company, Customer
from services.models import Service, ServiceRequest

def home(request):
    return render(request, 'main/home.html', {})

def _calc_age(dob):
    if not dob:
        return None
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

def customer_profile(request, name):
    user = get_object_or_404(User, username=name)
    customer = get_object_or_404(Customer, user=user)
    requests = ServiceRequest.objects.filter(customer=customer).order_by('-created_at')
    age = _calc_age(customer.date_of_birth)
    return render(request, 'users/profile.html', {'user': user, 'requests': requests, 'user_age': age})

def company_profile(request, name):
    user = get_object_or_404(User, username=name)
    company = get_object_or_404(Company, user=user)
    services = Service.objects.filter(company=company).order_by('-date')
    return render(request, 'users/profile.html', {'user': user, 'services': services})
