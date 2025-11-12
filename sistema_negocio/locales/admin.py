from django.contrib import admin

from .models import Local


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ("nombre", "direccion", "creado", "actualizado")
    search_fields = ("nombre", "direccion")
    list_filter = ("creado",)
