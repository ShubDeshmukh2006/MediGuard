from django.contrib import admin
from .models import Medicine, Interaction


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "requires_prescription", "source", "created_at")
    list_filter = ("category", "requires_prescription", "source")
    search_fields = ("name", "brand_names")


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("medicine_1", "medicine_2", "severity", "source", "created_at")
    list_filter = ("severity", "source")
    search_fields = ("medicine_1__name", "medicine_2__name")
