# Generated by Django 2.2.4 on 2020-09-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0010_mapfoodgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='activated',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='name_en',
            field=models.CharField(default='food_name_en', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='mapfoodgroup',
            name='alim_group_level',
            field=models.CharField(choices=[('grp', 'grp'), ('ss_grp', 'ss_grp'), ('ss_ss_grp', 'ss_ss_grp')], max_length=150),
        ),
    ]
