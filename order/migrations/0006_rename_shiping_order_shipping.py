# Generated by Django 3.2.3 on 2021-06-03 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210603_1250'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='shiping',
            new_name='shipping',
        ),
    ]
