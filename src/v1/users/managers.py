from typing import Any

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    @staticmethod
    def email_validator(email: str) -> bool:
        try:
            validate_email(email)
            return True
        except ValidationError:
            raise ValueError(_("You must provide a valid email address."))

    def create_user(self, name: str, email: str, password: str, **extra_fields: Any):
        if not name:
            raise ValueError(_("User must have a name."))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("User must have an email address."))

        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user.save()
        return user

    def create_superuser(self, name: str, email: str, password: str, **extra_fields: Any):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        if not password:
            raise ValueError(_("Superuser must have a password."))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Superuser must have an email address."))

        user = self.create_user(name=name, email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user
