# Generated by Django 4.1.4 on 2023-01-30 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0028_remove_order_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pin_code',
            field=models.CharField(default='', max_length=50),
        ),
    ]