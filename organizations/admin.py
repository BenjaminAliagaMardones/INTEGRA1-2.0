from django.contrib import admin
from .models import Company, Cooperative


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'created_by', 'members_count', 'created_at']
    list_filter = ['sector', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'sector', 'created_by', 'companies_count', 'created_at']
    list_filter = ['sector', 'created_at']
    search_fields = ['name', 'description']

