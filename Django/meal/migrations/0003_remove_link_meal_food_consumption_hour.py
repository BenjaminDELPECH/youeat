# Generated by Django 2.2.4 on 2020-03-09 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meal', '0002_link_meal_food_consumption_hour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='link_meal_food',
            name='consumption_hour',
        ),
    ]
