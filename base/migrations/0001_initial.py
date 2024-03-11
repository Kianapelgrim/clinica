# Generated by Django 5.0.3 on 2024-03-08 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Surcursales',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
                ('direccion', models.TextField()),
                ('correoElectronico', models.EmailField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
    ]
