# Generated by Django 5.0.3 on 2024-04-27 22:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0072_parametros_next_invoice_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='ISV',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='base.pacientes', unique=True)),
                ('creado', models.DateField(auto_now_add=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.DateField(auto_now_add=True),
        ),
    ]
