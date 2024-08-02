from django.db import models
from django.db.models import Count


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return self.annotate(count_orders=Count('profile_orders')).filter(count_orders__gt=2).order_by('-count_orders')