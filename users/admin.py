
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Company

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','groups','user_permissions','is_company','is_customer')}),
        ('Important dates', {'fields': ('last_login','date_joined')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',),'fields': ('email','username','password1','password2')}),
    )
    list_display = ('email','username','is_company','is_customer','is_staff')
    search_fields = ('email','username')
    ordering = ('email',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','date_of_birth')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('user','field_of_work')
