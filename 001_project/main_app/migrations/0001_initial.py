# Generated by Django 5.0.4 on 2024-06-21 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('code', models.CharField(max_length=4, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('employees_count', models.PositiveIntegerField(default=1, verbose_name='Employees Count')),
                ('location', models.CharField(blank=True, choices=[('Sofia', 'Sofia'), ('Plovdiv', 'Plovdiv'), ('Burgas', 'Burgas'), ('Varna', 'Varna')], max_length=20, null=True)),
                ('last_edited_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
