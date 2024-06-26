# Generated by Django 5.0.3 on 2024-04-17 00:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0057_remove_detallepedido_fechavencimiento_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventariomedicamento',
            name='lote',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.lotemedicamento'),
        ),
        migrations.AddField(
            model_name='lotemedicamento',
            name='medicamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.medicamentos'),
        ),
        migrations.AlterField(
            model_name='inventariomedicamento',
            name='medicamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='base.medicamentos'),
        ),
    ]
