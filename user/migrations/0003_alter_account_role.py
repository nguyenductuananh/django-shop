# Generated by Django 3.2.3 on 2021-06-17 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_account_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.IntegerField(choices=[(1, 'Staff'), (2, 'Business'), (3, 'Sale'), (0, 'Customer')], default=0),
        ),
    ]
