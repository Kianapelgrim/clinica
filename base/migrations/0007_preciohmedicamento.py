# Generated by Django 5.0.3 on 2024-03-15 02:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_ecmedicamentos'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrecioHMedicamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField()),
                ('fechaFinal', models.DateField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.medicamentos')),
                ('surcursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.surcursales')),
            ],
        ),
    ]
