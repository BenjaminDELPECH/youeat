# Generated by Django 2.2.4 on 2020-03-01 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0004_food_foodgroup'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversionfactor',
            name='conversion_factor',
        ),
    ]
