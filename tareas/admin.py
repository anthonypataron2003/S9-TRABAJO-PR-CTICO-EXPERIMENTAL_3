from django.contrib import admin

from .models import Tarea


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "estado", "creada")
    list_filter = ("estado", "creada")
    search_fields = ("titulo",)
