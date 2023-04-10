from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type_id',
                    'phone_number',]


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['user_type']
