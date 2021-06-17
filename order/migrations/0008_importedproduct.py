# Generated by Django 3.2.3 on 2021-06-09 07:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('order', '0007_auto_20210608_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importPrice', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('date', models.DateTimeField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.supplier')),
            ],
            options={
                'verbose_name': 'ImportedProduct',
                'verbose_name_plural': 'ImportedProducts',
            },
        ),
    ]
