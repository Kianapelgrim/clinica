# Generated by Django 5.0.3 on 2024-04-16 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0043_alter_parametros_surcursal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametros',
            name='correoElectronico',
            field=models.EmailField(max_length=254),
        ),
    ]