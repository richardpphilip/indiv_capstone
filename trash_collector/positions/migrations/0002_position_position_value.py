# Generated by Django 3.1.7 on 2021-06-01 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('positions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='position_value',
            field=models.IntegerField(default=0, null=True),
        ),
    ]