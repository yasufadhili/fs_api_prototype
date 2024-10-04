from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, EmailValidator
from django.conf import settings
from django.utils.translation import get_language
import shortuuid
from django_countries.fields import CountryField
from accounts.managers import CustomUserManager

USERNAME_VALIDATOR = RegexValidator(
    regex=r'^[a-zA-Z0-9_.-]+$',
    message='Username must be alphanumeric, with no spaces.'
)

PHONE_NUMBER_VALIDATOR = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

LANGUAGES = (
    ('en', 'English'),
    ('sw', 'Swahili'),
    ('ar', 'Arabic'),
    ('pt', 'Portuguese'),
    ('it', 'Italian'),
    ('nl', 'Dutch'),
    ('ru', 'Russian'),
    ('fr', 'French'),
    ('de', 'German'),
    ('es', 'Spanish'),
)

class User(AbstractUser):
    """Custom User model"""
    REGULAR = 'REGULAR'
    FOOTBALLER = 'FOOTBALLER'
    MANAGER = 'MANAGER'
    ORGANISATION = 'ORGANISATION'
    
    USER_TYPES = (
        (REGULAR, 'Regular User'),
        (FOOTBALLER, 'Footballer User'),
        (MANAGER, 'Manager User'),
        (ORGANISATION, 'Organisation (Broadcaster/News Agency)'),
    )

    id = models.CharField(
        _("id"),
        primary_key=True,
        max_length=255,
        default=shortuuid.uuid,
        help_text=_("User ID"),
        db_index=True
    )
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[EmailValidator()]
    )
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[PHONE_NUMBER_VALIDATOR],
        verbose_name=_("Phone number")
    )
    username = models.CharField(
        unique=True,
        max_length=100,
        validators=[USERNAME_VALIDATOR],
        verbose_name=_("Username")
    )
    firstname = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("First name")
    )
    lastname = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name=_("Last name")
    )
    user_type = models.CharField(
        max_length=50,
        choices=USER_TYPES,
        default=REGULAR,
        verbose_name=_("User Type")
    )
    is_moderator = models.BooleanField(default=False)
    is_developer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    user_relationships = models.ManyToManyField(
        "self",
        through="UserRelationship",
        symmetrical=False,
        related_name="related_to",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "phone_number"]

    def get_followers(self):
        return self.followers.all()

    def get_following(self):
        return self.following.all()

    def __str__(self):
        return self.username

class UserRelationship(models.Model):
    """Model to define follower-following relationships between users"""
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.follower} follows {self.following}"

class BaseProfile(models.Model):
    """Base Profile model with common fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=1000)
    avatar = models.URLField(blank=True, null=True)
    status = models.ForeignKey("ProfileStatus", blank=True, null=True, on_delete=models.CASCADE, related_name="%(class)s_status")
    preferred_language = models.CharField(choices=LANGUAGES, default='en', max_length=100, blank=True)
    time_zone = models.CharField(max_length=100, blank=True, verbose_name="Time zone")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    website = models.URLField(blank=True, null=True)
    social_media_links = models.JSONField(blank=True, null=True)

    class Meta:
        abstract = True

    def get_preferred_language(self):
        return self.preferred_language or get_language()

    def get_time_zone(self):
        return self.time_zone or settings.TIME_ZONE

    def followers_count(self):
        return self.user.followers.count()

    def following_count(self):
        return self.user.following.count()

class RegularProfile(BaseProfile):
    """Profile for regular users"""
    pass

class FootballerProfile(BaseProfile):
    """Profile for footballer users"""
    position = models.CharField(max_length=100, blank=True, null=True)
    club = models.CharField(max_length=255, blank=True, null=True)
    national_team = models.CharField(max_length=255, blank=True, null=True)

class ManagerProfile(BaseProfile):
    """Profile for manager users"""
    current_team = models.CharField(max_length=255, blank=True, null=True)
    coaching_style = models.CharField(max_length=255, blank=True, null=True)

class OrganisationProfile(BaseProfile):
    """Profile for organisation users"""
    organisation_name = models.CharField(max_length=255, blank=True, null=True)
    organisation_type = models.CharField(max_length=255, blank=True, null=True)

class ProfileStatus(models.Model):
    """Statuses for user profiles"""
    regular_profile = models.ForeignKey(RegularProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='statuses')
    footballer_profile = models.ForeignKey(FootballerProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='statuses')
    manager_profile = models.ForeignKey(ManagerProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='statuses')
    organisation_profile = models.ForeignKey(OrganisationProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='statuses')
    status = models.CharField(choices=(
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('banned', 'Banned'),
    ), default='active', max_length=100, blank=True)
    reason = models.TextField(blank=True, null=True, max_length=1000)
    reconsidered_at = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile Status")
        verbose_name_plural = _("Profile Statuses")

    def __str__(self):
        return self.status

    @property
    def profile(self):
        return self.regular_profile or self.footballer_profile or self.manager_profile or self.organisation_profile
