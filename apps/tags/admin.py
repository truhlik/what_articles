from django.contrib import admin

from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name_en', 'name_de']
    search_fields = ['name_en', 'name_de']
