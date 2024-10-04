from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, UserRelationship, RegularProfile, FootballerProfile,
    ManagerProfile, OrganisationProfile, ProfileStatus
)

class UserRelationshipInline(admin.TabularInline):
    model = UserRelationship
    fk_name = 'follower'
    extra = 1
    verbose_name = _("Following")
    verbose_name_plural = _("Following")

class ProfileStatusInline(admin.TabularInline):
    model = ProfileStatus
    extra = 1

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields['regular_profile'].initial = obj if isinstance(obj, RegularProfile) else None
            formset.form.base_fields['footballer_profile'].initial = obj if isinstance(obj, FootballerProfile) else None
            formset.form.base_fields['manager_profile'].initial = obj if isinstance(obj, ManagerProfile) else None
            formset.form.base_fields['organisation_profile'].initial = obj if isinstance(obj, OrganisationProfile) else None
        return formset

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'firstname', 'lastname', 'user_type', 'is_verified', 'is_staff')
    list_filter = ('user_type', 'is_verified', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('firstname', 'lastname', 'email', 'phone_number')}),
        (_('User details'), {'fields': ('user_type', 'is_verified')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'password1', 'password2', 'user_type'),
        }),
    )
    search_fields = ('username', 'firstname', 'lastname', 'email')
    ordering = ('username',)
    inlines = [UserRelationshipInline]

    def get_inlines(self, request, obj=None):
        if obj:
            return [UserRelationshipInline]
        return []

class BaseProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'preferred_language', 'time_zone')
    list_filter = ('country', 'preferred_language', 'time_zone')
    search_fields = ('user__username', 'user__email', 'bio')
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

@admin.register(UserRelationship)
class UserRelationshipAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('follower__username', 'following__username')
    date_hierarchy = 'created_at'

@admin.register(ProfileStatus)
class ProfileStatusAdmin(admin.ModelAdmin):
    list_display = ('get_profile', 'status', 'created_at', 'updated_at', 'reconsidered_at')
    list_filter = ('status', 'created_at', 'updated_at', 'reconsidered_at')
    search_fields = ('regular_profile__user__username', 'footballer_profile__user__username', 
                     'manager_profile__user__username', 'organisation_profile__user__username', 'reason')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

    def get_profile(self, obj):
        return obj.profile
    get_profile.short_description = 'Profile'

# Unregister the Group model from admin.
from django.contrib.auth.models import Group
admin.site.unregister(Group)