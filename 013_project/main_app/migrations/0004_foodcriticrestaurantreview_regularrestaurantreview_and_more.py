# Generated by Django 5.0.4 on 2024-07-21 19:53

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_restaurantreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCriticRestaurantReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_name', models.CharField(max_length=100)),
                ('review_content', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('food_critic_cuisine_area', models.CharField(max_length=100)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.restaurant')),
            ],
            options={
                'verbose_name': 'Food Critic Review',
                'verbose_name_plural': 'Food Critic Reviews',
                'ordering': ('-rating',),
                'abstract': False,
                'unique_together': {('reviewer_name', 'restaurant')},
            },
        ),
        migrations.CreateModel(
            name='RegularRestaurantReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_name', models.CharField(max_length=100)),
                ('review_content', models.TextField()),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.restaurant')),
            ],
            options={
                'verbose_name': 'Restaurant Review',
                'verbose_name_plural': 'Restaurant Reviews',
                'ordering': ('-rating',),
                'abstract': False,
                'unique_together': {('reviewer_name', 'restaurant')},
            },
        ),
        migrations.DeleteModel(
            name='RestaurantReview',
        ),
    ]
