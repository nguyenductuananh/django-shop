# Generated by Django 3.2.3 on 2021-06-15 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.IntegerField(choices=[('Staff', 1), ('Business', 2), ('Sale', 3), ('Customer', 0)], default=0),
        ),
    ]
