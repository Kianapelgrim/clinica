# Generated by Django 5.0.3 on 2024-04-04 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_surcursales_personaencargada'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedores',
            name='personaEncargada',
            field=models.CharField(max_length=255, null=True),
        ),
    ]