# Generated by Django 2.2.4 on 2020-03-01 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_auto_20200301_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='foodGroup',
        ),
    ]
