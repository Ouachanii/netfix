
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

class User(AbstractUser):
    is_company = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # username still required for display

    def __str__(self):
        return self.username or self.email

FIELD_OF_WORK_CHOICES = [
    ('Air Conditioner','Air Conditioner'),
    ('All in One','All in One'),
    ('Carpentry','Carpentry'),
    ('Electricity','Electricity'),
    ('Gardening','Gardening'),
    ('Home Machines','Home Machines'),
    ('Housekeeping','Housekeeping'),
    ('Interior Design','Interior Design'),
    ('Locks','Locks'),
    ('Painting','Painting'),
    ('Plumbing','Plumbing'),
    ('Water Heaters','Water Heaters'),
]

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    date_of_birth = models.DateField()

    def __str__(self):
        return f"Customer({self.user})"

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    field_of_work = models.CharField(max_length=40, choices=FIELD_OF_WORK_CHOICES)

    def __str__(self):
        return f"Company({self.user})"
