# Generated by Django 4.1.4 on 2023-01-30 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('read', '0023_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='accountopen',
        ),
    ]
