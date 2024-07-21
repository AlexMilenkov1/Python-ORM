from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Index

from validators import validate_menu_categories


# Create your models here.
class ReviewMixIn(models.Model):
    reviewer_name = models.CharField(max_length=100)
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    class Meta:
        abstract = True
        ordering = ('-rating', )


class Restaurant(models.Model):
    name = models.CharField(validators=[
        MinLengthValidator(2, 'Name must be at least 2 characters long.'),
        MaxLengthValidator(100, 'Name cannot exceed 100 characters.')
    ])

    location = models.CharField(validators=[
        MinLengthValidator(2, 'Location must be at least 2 characters long.'),
        MaxLengthValidator(200, 'Location cannot exceed 200 characters.')
    ])

    description = models.TextField(blank=True, null=True)

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0, 'Rating must be at least 0.00.'),
            MaxValueValidator(5, 'Rating cannot exceed 5.00.')
        ])


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(validators=[validate_menu_categories])
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class RestaurantReview(ReviewMixIn):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta(ReviewMixIn.Meta):
        abstract = True
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ['reviewer_name', 'restaurant']


class RegularRestaurantReview(RestaurantReview):
    pass


class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField(max_length=100)

    class Meta(RestaurantReview.Meta):
        verbose_name = 'Food Critic Review'
        verbose_name_plural = 'Food Critic Reviews'


class MenuReview(ReviewMixIn):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta(ReviewMixIn.Meta):
        verbose_name = 'Menu Review'
        verbose_name_plural = 'Menu Reviews'
        unique_together = ['reviewer_name', 'menu']
        indexes = [
            models.Index(
                fields=['menu'],
                name='main_app_menu_review_menu_id')
        ]
