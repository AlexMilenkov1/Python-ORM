from django.db import models


class GenreChoices(models.TextChoices):
    Action = 'Action', 'Action'
    Comedy = 'Comedy', 'Comedy'
    Drama = 'Drama', 'Drama'
    Other = 'Other', 'Other'

