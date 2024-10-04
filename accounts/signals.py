
from .models import RegularProfile, Account, FootballerProfile, ManagerProfile, OrganisationProfile
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Account)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.account_type == Account.REGULAR:
            RegularProfile.objects.create(account=instance)
        elif instance.account_type == Account.FOOTBALLER and instance.is_verified:
            FootballerProfile.objects.create(account=instance)
        elif instance.account_type == Account.MANAGER and instance.is_verified:
            ManagerProfile.objects.create(account=instance)
        elif instance.account_type == Account.ORGANISATION and instance.is_verified:
            OrganisationProfile.objects.create(account=instance)
    else:
        if instance.is_verified:
            if instance.account_type == Account.FOOTBALLER and not hasattr(instance, 'footballerprofile'):
                FootballerProfile.objects.create(account=instance)
            elif instance.account_type == Account.MANAGER and not hasattr(instance, 'managerprofile'):
                ManagerProfile.objects.create(account=instance)
            elif instance.account_type == Account.ORGANISATION and not hasattr(instance, 'organisationprofile'):
                OrganisationProfile.objects.create(account=instance)