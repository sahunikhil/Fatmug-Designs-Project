# Generated by Django 4.2.7 on 2023-12-04 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms_pm', '0009_alter_purchaseorder_delivery_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='contact_details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
