
from django import forms
from users.models import Company
from .models import SERVICE_FIELD_CHOICES

class CreateNewService(forms.Form):
    name = forms.CharField(max_length=40)
    description = forms.CharField(widget=forms.Textarea, label='Description')
    price_hour = forms.DecimalField(decimal_places=2, max_digits=8, min_value=0.00)
    field = forms.ChoiceField(required=True, choices=SERVICE_FIELD_CHOICES)

    def __init__(self, *args, **kwargs):
        super(CreateNewService, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Service Name'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter Description'
        self.fields['price_hour'].widget.attrs['placeholder'] = 'Enter Price per Hour'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'

class RequestServiceForm(forms.Form):
    address = forms.CharField(max_length=255)
    hours = forms.DecimalField(decimal_places=1, max_digits=5, min_value=0.5)

    def __init__(self, *args, **kwargs):
        super(RequestServiceForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs['placeholder'] = 'Service Address'
        self.fields['hours'].widget.attrs['placeholder'] = 'Number of hours'
