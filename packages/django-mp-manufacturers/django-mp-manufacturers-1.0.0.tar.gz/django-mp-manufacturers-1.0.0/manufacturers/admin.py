
from django.contrib import admin

from manufacturers.models import Manufacturer


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'new_name', 'has_supplier', 'logo']
    search_fields = ['name', 'new_name']
    list_editable = ['new_name']
    list_per_page = 100
