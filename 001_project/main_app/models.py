from datetime import date

from django.db import models

#
# class Employee(models.Model):
#     name = models.CharField(max_length=30)
#     email_address = models.EmailField()
#     photo = models.URLField()
#     birth_date = models.DateField(auto_now=True)
#     works_full_time = models.BooleanField()
#     created_on = models.DateTimeField(auto_now_add=True)
#
#
# class Department(models.Model):
#     class CityChoices(models.TextChoices):
#         SOFIA = "Sofia", "Sofia"
#         PLOVDIV = "Plovdiv", "Plovdiv"
#         BURGAS = "Burgas", "Burgas"
#         VARNA = "Varna", "Varna"
#
#     code = models.CharField(max_length=4, primary_key=True, unique=True)
#     name = models.CharField(max_length=50, unique=True)
#     employees_count = models.PositiveIntegerField(default=1, verbose_name="Employees Count")
#     location = models.CharField(max_length=20, blank=True, null=True, choices=CityChoices)
#     last_edited_on = models.DateTimeField(auto_now=True, editable=False)


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    duration_in_days = models.PositiveIntegerField(blank=True, null=True, verbose_name="Duration in Days")
    estimated_hours = models.FloatField(blank=True, null=True, verbose_name="Estimated Hours")
    start_date = models.DateField(verbose_name="Start Date", blank=True, null=True, default=date.today)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    last_edited_on = models.DateTimeField(auto_now=True, editable=False)
