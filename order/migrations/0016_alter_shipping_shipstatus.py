# Generated by Django 3.2.3 on 2021-06-17 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0015_alter_shipping_shipstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipping',
            name='shipStatus',
            field=models.IntegerField(choices=[(1, 'SHIPPING'), (2, 'DONE'), (0, 'PROCESSING')], default=0),
        ),
    ]
