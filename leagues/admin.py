from django.contrib import admin
from .models import League

class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'country', 'continent', 'year_established')
    list_filter = ('continent', 'country')
    search_fields = ('name', 'short_name', 'country__name', 'year_established')

admin.site.register(League, LeagueAdmin)