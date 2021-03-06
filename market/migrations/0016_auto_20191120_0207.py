# Generated by Django 2.2.5 on 2019-11-20 07:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0015_auto_20191114_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrequest',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(choices=[(1, 'Closed: Sold in Marketplace'), (2, 'Closed: Sold outside Marketplace')], default=1),
        ),
    ]
