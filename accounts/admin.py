from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    Account, AccountRelationship, RegularProfile, FootballerProfile,
    ManagerProfile, OrganisationProfile, ProfileStatus
)

class AccountRelationshipInline(admin.TabularInline):
    model = AccountRelationship
    fk_name = 'follower'
    extra = 1
    verbose_name = _("Following")
    verbose_name_plural = _("Following")

class ProfileStatusInline(admin.TabularInline):
    model = ProfileStatus
    extra = 1

@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'firstname', 'lastname', 'account_type', 'is_verified', 'is_staff')
    list_filter = ('account_type', 'is_verified', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('firstname', 'lastname', 'email', 'phone_number')}),
        (_('Account details'), {'fields': ('account_type', 'is_verified')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'account_type'),
        }),
    )
    search_fields = ('username', 'firstname', 'lastname', 'email')
    ordering = ('username',)
    inlines = [AccountRelationshipInline]

    def get_inlines(self, request, obj=None):
        if obj:
            return [AccountRelationshipInline]
        return []

class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ('account', 'country', 'preferred_language', 'time_zone')
    list_filter = ('country', 'preferred_language', 'time_zone')
    search_fields = ('account__username', 'account__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProfileStatusInline]

@admin.register(RegularProfile)
class RegularProfileAdmin(BaseProfileAdmin):
    pass

@admin.register(FootballerProfile)
class FootballerProfileAdmin(BaseProfileAdmin):
    list_display = BaseProfileAdmin.list_display + ('position', 'club', 'national_team')
    list_filter = BaseProfileAdmin.list_filter + ('position', 'club', 'national_team')
    search_fields = BaseProfileAdmin.search_fields + ('position', 'club', 'national_team')

@admin.register(ManagerProfile)
class ManagerProfileAdmin(BaseProfileAdmin):
    list_display = BaseProfileAdmin.list_display + ('current_team', 'coaching_style')
    list_filter = BaseProfileAdmin.list_filter + ('current_team', 'coaching_style')
    search_fields = BaseProfileAdmin.search_fields + ('current_team', 'coaching_style')

@admin.register(OrganisationProfile)
class OrganisationProfileAdmin(BaseProfileAdmin):
    list_display = BaseProfileAdmin.list_display + ('organisation_name', 'organisation_type')
    list_filter = BaseProfileAdmin.list_filter + ('organisation_type',)
    search_fields = BaseProfileAdmin.search_fields + ('organisation_name', 'organisation_type')

@admin.register(AccountRelationship)
class AccountRelationshipAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    date_hierarchy = 'created_at'

@admin.register(ProfileStatus)
class ProfileStatusAdmin(admin.ModelAdmin):
    list_display = ('profile', 'status', 'created_at', 'updated_at', 'reconsidered_at')
    list_filter = ('status', 'created_at', 'updated_at', 'reconsidered_at')
    search_fields = ('profile__account__username', 'reason')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

# Unregister the Group model from admin.
# If you want to use it, you can comment out this line
from django.contrib.auth.models import Group
admin.site.unregister(Group)