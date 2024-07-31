from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.choices import GenreChoices
from main_app.managers import DirectorManager


# Create your models here.
class BasePeople(models.Model):
    full_name = models.CharField(
        max_length=120,
        validators=[
            MinLengthValidator(2)
        ]
    )

    birth_date = models.DateField(
        default='1900-01-01'
    )

    nationality = models.CharField(
        max_length=50,
        default='Unknown'
    )

    class Meta:
        abstract = True


class AwardedMixin(models.Model):
    is_awarded = models.BooleanField(default=False)

    class Meta:
        abstract = True


class UpdatedMixin(models.Model):
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Director(BasePeople):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )

    objects = DirectorManager()


class Actor(BasePeople, AwardedMixin, UpdatedMixin):
    pass


class Movie(AwardedMixin, UpdatedMixin):
    title = models.CharField(
        max_length=150,
        validators=[
            MinLengthValidator(5)
        ]
    )

    release_date = models.DateField()

    storyline = models.TextField(
        blank=True,
        null=True
    )

    genre = models.CharField(
        max_length=6,
        choices=GenreChoices,
        default='Other'
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        default=0
    )

    is_classic = models.BooleanField(default=False)

    director = models.ForeignKey(Director, on_delete=models.CASCADE, related_name='director_movies')

    starring_actor = models.ForeignKey(
        Actor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='starring_movies'
    )

    actors = models.ManyToManyField(Actor, related_name='movies')
