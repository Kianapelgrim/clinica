# Generated by Django 5.0.3 on 2024-04-28 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0084_alter_proveedores_personaencargada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surcursales',
            name='personaEncargada',
            field=models.CharField(max_length=255),
        ),
    ]