import os
from datetime import date
from pprint import pprint

import django
from django.db import connection
from django.db.models import Count, Max

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import RealEstateListing, VideoGame, Invoice, BillingInfo, Technology, Programmer, Project, Task


