# Generated by Django 5.1.5 on 2025-04-19 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend_1', '0006_alter_driver_is_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.CharField(max_length=100),
        ),
    ]
