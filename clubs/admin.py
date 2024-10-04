from django.contrib import admin
from .models import Club
from leagues.models import League

class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'full_name', 'year_established', 'league')
    list_filter = ('league',)
    search_fields = ('name', 'short_name', 'full_name', 'year_established')


admin.site.register(Club, ClubAdmin)