from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Customer, UserAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)