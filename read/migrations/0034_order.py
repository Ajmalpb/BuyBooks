# Generated by Django 4.1.4 on 2023-02-02 06:26

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0033_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('address', models.CharField(default='', max_length=200)),
                ('phone', models.CharField(default='', max_length=50)),
                ('pincode', models.CharField(default='', max_length=50)),
                ('date', models.DateField(default=datetime.datetime.today, max_length=50)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='read.registration')),
            ],
        ),
    ]
