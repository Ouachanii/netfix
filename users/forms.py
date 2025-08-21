
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login

from .models import User, Company, Customer, FIELD_OF_WORK_CHOICES

class DateInput(forms.DateInput):
    input_type = 'date'

def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Email already registered.')

def validate_username(value):
    if User.objects.filter(username=value).exists():
        raise ValidationError('Username already taken.')

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    username = forms.CharField(max_length=150, validators=[validate_username])
    date_of_birth = forms.DateField(widget=DateInput)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email','username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.is_customer = True
        user.is_company = False
        if commit:
            user.save()
            Customer.objects.create(user=user, date_of_birth=self.cleaned_data['date_of_birth'])
        return user

class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(validators=[validate_email])
    username = forms.CharField(max_length=150, validators=[validate_username])
    field_of_work = forms.ChoiceField(choices=FIELD_OF_WORK_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email','username',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.is_company = True
        user.is_customer = False
        if commit:
            user.save()
            Company.objects.create(user=user, field_of_work=self.cleaned_data['field_of_work'])
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Enter Email', 'autocomplete':'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email')
        password = cleaned.get('password')
        if email and password:
            try:
                user = User.objects.get(email=email)
                auth_user = authenticate(username=email, password=password)
                if auth_user is None:
                    raise ValidationError('Invalid email/password.')
            except User.DoesNotExist:
                raise ValidationError('Invalid email/password.')
        return cleaned
