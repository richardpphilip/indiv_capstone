# Generated by Django 3.1.7 on 2021-05-27 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='portfolio_balance',
            field=models.IntegerField(default=0),
        ),
    ]
