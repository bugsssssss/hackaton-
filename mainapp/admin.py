from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'user_type_id',
                    'phone_number1',]


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['user_type']


admin.site.register(Skills)


admin.site.register(Category)
admin.site.register(Order)
admin.site.register(ActiveOrder)
admin.site.register(ServiceType)
admin.site.register(Service)
