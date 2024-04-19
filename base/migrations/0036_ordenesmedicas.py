# Generated by Django 5.0.3 on 2024-04-14 00:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0035_remove_prescripciones_paciente'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenesMedicas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('indicaciones', models.TextField(blank=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('cita', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.citas')),
            ],
        ),
    ]
