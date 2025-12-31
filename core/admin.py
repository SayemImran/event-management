from django.contrib import admin
from core.models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        (None,{'fields':('username','password')}),
        ('Personal Info',{'fields':('first_name','last_name','email','profile_image','phone_number')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Importants Dates',{'fields':('last_login','date_joined')}),
    )