from django.contrib import admin
from .models import DynamicTable, DynamicField

@admin.register(DynamicTable)
class DynamicTableAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("-created_at",)


@admin.register(DynamicField)
class DynamicFieldAdmin(admin.ModelAdmin):
    list_display = ("table", "field_name", "field_type")
    search_fields = ("field_name",)
    list_filter = ("field_type",)

