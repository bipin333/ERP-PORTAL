# Generated by Django 5.0.3 on 2024-04-21 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_mark_result'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mark',
            name='semester',
        ),
    ]