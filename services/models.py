
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from users.models import Company, Customer, FIELD_OF_WORK_CHOICES

SERVICE_FIELD_CHOICES = [c for c in FIELD_OF_WORK_CHOICES if c[0] != 'All in One']

class Service(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    description = models.TextField()
    price_hour = models.DecimalField(decimal_places=2, max_digits=8)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    field = models.CharField(max_length=40, choices=SERVICE_FIELD_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.field})"

class ServiceRequest(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    hours = models.DecimalField(decimal_places=1, max_digits=5, validators=[MinValueValidator(0.5)])
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def cost(self):
        return float(self.hours) * float(self.service.price_hour)

    def __str__(self):
        return f"{self.customer.user} -> {self.service.name} ({self.hours}h)"
