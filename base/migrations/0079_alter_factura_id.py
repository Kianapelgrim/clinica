# Generated by Django 5.0.3 on 2024-04-28 01:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0078_detallefactura'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.citas'),
        ),
    ]
