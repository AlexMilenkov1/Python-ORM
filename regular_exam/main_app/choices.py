from django.db import models


class StatusChoices(models.TextChoices):
    Planned = 'Planned', 'Planned'
    Ongoing = 'Ongoing', 'Ongoing'
    Completed = 'Completed', 'Completed'
