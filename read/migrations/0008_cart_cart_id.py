# Generated by Django 4.1.4 on 2023-01-16 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0007_alter_cart_prodect_id_alter_cart_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]