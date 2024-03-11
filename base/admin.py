from django.contrib import admin
from .models import Surcursales

@admin.register(Surcursales)
class SurcursalesAdmin(admin.ModelAdmin):
    pass
# Register your models here.
