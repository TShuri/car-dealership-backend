from django.contrib import admin
from .models import Car, Client, Deal, Employee, Service

# Register your models here.
admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Deal)
admin.site.register(Employee)
admin.site.register(Service)