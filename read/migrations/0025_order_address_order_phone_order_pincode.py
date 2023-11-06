# Generated by Django 4.1.4 on 2023-01-30 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0024_remove_order_accountopen'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='order',
            name='pincode',
            field=models.IntegerField(default=''),
        ),
    ]