# Generated by Django 5.0.3 on 2024-04-17 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_files_subject_materials'),
    ]

    operations = [
        migrations.AddField(
            model_name='files',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
