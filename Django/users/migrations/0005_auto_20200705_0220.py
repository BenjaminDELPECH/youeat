# Generated by Django 2.2.4 on 2020-07-05 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200629_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='carbohydrateProportion',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='fatProportion',
            field=models.IntegerField(default=35),
        ),
        migrations.AddField(
            model_name='profile',
            name='proteinProportion',
            field=models.IntegerField(default=15),
        ),
    ]
