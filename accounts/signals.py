
from .models import RegularProfile, User, FootballerProfile, ManagerProfile, OrganisationProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == User.REGULAR:
            RegularProfile.objects.create(user=instance)
        elif instance.user_type == User.FOOTBALLER and instance.is_verified:
            FootballerProfile.objects.create(user=instance)
        elif instance.user_type == User.MANAGER and instance.is_verified:
            ManagerProfile.objects.create(user=instance)
        elif instance.user_type == User.ORGANISATION and instance.is_verified:
            OrganisationProfile.objects.create(user=instance)
    else:
        if instance.is_verified:
            if instance.user_type == User.FOOTBALLER and not hasattr(instance, 'footballerprofile'):
                FootballerProfile.objects.create(user=instance)
            elif instance.user_type == User.MANAGER and not hasattr(instance, 'managerprofile'):
                ManagerProfile.objects.create(user=instance)
            elif instance.user_type == User.ORGANISATION and not hasattr(instance, 'organisationprofile'):
                OrganisationProfile.objects.create(user=instance)