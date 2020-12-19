# Generated by Django 3.0.5 on 2020-04-22 12:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='date_renwed',
        ),
        migrations.AddField(
            model_name='profile',
            name='date_renewed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 22, 17, 57, 15, 778667)),
        ),
        migrations.AlterField(
            model_name='groupinvitation',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 22, 17, 57, 15, 781692)),
        ),
        migrations.AlterField(
            model_name='grouprole',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 22, 17, 57, 15, 781692)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 22, 17, 57, 15, 777669)),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 22, 17, 57, 15, 777669)),
        ),
        migrations.AlterField(
            model_name='plan',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 4, 22, 17, 57, 15, 775675)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
