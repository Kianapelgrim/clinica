# Generated by Django 5.0.3 on 2024-04-16 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0050_remove_medicamentos_precio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preciohmedicamento',
            name='surcursal',
        ),
    ]