from django.core import validators
from django.db import models
from django.forms import CharField, forms
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(
        _("email"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @ and . only."
        ),
        validators = [],
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )
    username = models.CharField(max_length=100, default="")
    def get_absolute_url(self):
        return reverse('user_profile_detail', args=[self.pk])  # Возвращаем URL для деталей профиля пользователя

    def save(self, *args, **kwargs):
        if not self.pk:
            # Проверяем, существует ли уже пользователь с таким email адресом
            if UserProfile.objects.filter(email=self.email).exists():
                raise ValueError('A user with that email already exists.')
        return super().save(*args, **kwargs)

class EmailField(CharField):
    default_validators = [validators.validate_email]
    description = _("Email address")

    def __init__(self, *args, **kwargs):
        # max_length=254 to be compliant with RFCs 3696 and 5321
        kwargs.setdefault("max_length", 254)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # We do not exclude max_length if it matches default as we want to change
        # the default in future.
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        # As with CharField, this will cause email validation to be performed
        # twice.
        return super().formfield(
            **{
                "form_class": forms.EmailField,
                **kwargs,
            }


        )




