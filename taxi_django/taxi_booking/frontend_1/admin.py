from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer
from .models import *

class CustomerAdmin(UserAdmin):
    list_display = ('customer_username', 'customer_email', 'is_staff')
    search_fields = ('customer_username', 'customer_email')
    ordering = ('customer_username',)
    fieldsets = (
        (None, {'fields': ('customer_username', 'customer_password')}),
        ('Personal info', {'fields': ('customer_name', 'customer_email', 'customer_mobile', 'customer_city')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(Customer, CustomerAdmin)

admin.site.register(Vehicle)
admin.site.register(Driver)
admin.site.register(feedback)
admin.site.register(Payment)
admin.site.register(Booking)
