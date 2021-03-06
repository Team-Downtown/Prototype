# Generated by Django 2.2.5 on 2019-11-12 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0012_auto_20191030_1341'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='status',
            field=models.IntegerField(choices=[(1, 'Sold in Marketplace'), (2, 'Sold outside Marketplace'), (3, 'Closed')], default=1),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_closed',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
