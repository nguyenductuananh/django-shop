# Generated by Django 3.2.3 on 2021-06-03 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('order', '0002_notificationaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='person',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.person'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paymentMethod',
            field=models.CharField(choices=[('BANK', 'BANK'), ('COD', 'COD')], max_length=200),
        ),
    ]
