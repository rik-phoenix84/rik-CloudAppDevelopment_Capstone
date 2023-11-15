from django.contrib import admin
from .models import *


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['carmake', 'name', 'dealer_id', 'car_type', 'year']
    list_filter = ['car_type', 'carmake', 'dealer_id', 'year',]
    search_fields = ['carmake', 'name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
