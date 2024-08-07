# Generated by Django 5.0.4 on 2024-07-23 09:29

import django.core.validators
import validations
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[validations.contain_only_letters_and_spaces])),
                ('age', models.PositiveIntegerField(validators=[validations.age_validation])),
                ('email', models.EmailField(error_messages={'invalid': 'Enter a valid email address'}, max_length=254)),
                ('phone_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must start with '+359' followed by 9 digits", regex='^\\+359\\d{9}$')])),
                ('website_url', models.URLField(error_messages={'invalid': 'Enter a valid URL'})),
            ],
        ),
    ]
