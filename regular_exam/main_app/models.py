from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.db import models

from main_app.choices import StatusChoices
from main_app.managers import AstronautManager


# Create your models here.
class NameAndUpdate(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class LaunchMixin(models.Model):
    launch_date = models.DateField()

    class Meta:
        abstract = True


class Astronaut(NameAndUpdate):
    phone_number = models.CharField(
        unique=True,
        max_length=15,
        validators=[
            RegexValidator(r'^\d+$')
        ]
    )

    is_active = models.BooleanField(default=True)

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[
           MinValueValidator(0)
        ]
    )

    objects = AstronautManager()


class Spacecraft(NameAndUpdate, LaunchMixin):
    manufacturer = models.CharField(max_length=100)

    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1)
        ]
    )

    weight = models.FloatField(
        validators=[
            MinValueValidator(0.0)
        ]
    )


class Mission(NameAndUpdate, LaunchMixin):
    description = models.TextField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=9,
        default='Planned',
        choices=StatusChoices
    )

    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE, related_name='spacecraft_missions')
    astronauts = models.ManyToManyField(Astronaut, related_name='missions')
    commander = models.ForeignKey(
        Astronaut,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='commander_missions'
    )
















