# Generated by Django 2.2.5 on 2019-11-22 03:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0016_auto_20191120_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrequest',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_closed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(choices=[(1, 'Closed: Sold in Marketplace'), (2, 'Closed: Not Sold in Marketplace')], default=1),
        ),
    ]