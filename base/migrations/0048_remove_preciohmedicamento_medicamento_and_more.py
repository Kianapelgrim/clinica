# Generated by Django 5.0.3 on 2024-04-16 06:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0047_remove_medicamentos_precio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preciohmedicamento',
            name='medicamento',
        ),
        migrations.AddField(
            model_name='medicamentos',
            name='precio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.preciohmedicamento'),
        ),
    ]
