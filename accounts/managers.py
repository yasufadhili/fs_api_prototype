from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    """
    Custom manager for user model where email, username, and phone number
    are required fields. Handles both regular users and superusers.
    """
    def create_user(self, username, phone_number, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')

        if not phone_number:
            raise ValueError('The phone number must be set')

        if email:
            email = self.normalize_email(email)
        else:
            raise ValueError('The email must be set')

        if not password:
            raise ValueError('The password must be set')

        now = extra_fields.get("date_joined", timezone.now())
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)

        user = self.model(
            username=username,
            phone_number=phone_number,
            email=email,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)  # Always use 'self._db' for multi-database support

        return user

    def create_superuser(self, username, phone_number, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not email:
            raise ValueError('Superuser must have an email address')

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(username, phone_number, email, password, **extra_fields)
