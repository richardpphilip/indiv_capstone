# Generated by Django 3.1.7 on 2021-06-01 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('positions', '0002_position_position_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='stock_close_value',
            field=models.FloatField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='position_value',
            field=models.FloatField(default=0, null=True),
        ),
    ]
