# Generated by Django 4.1.4 on 2023-01-30 11:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0022_remove_cartitem_cart_remove_cartitem_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('accountopen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read.joining')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read.registration')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read.product')),
            ],
        ),
    ]