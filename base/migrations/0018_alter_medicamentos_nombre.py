# Generated by Django 5.0.3 on 2024-03-24 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_remove_inventariomedicamento_surcursal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicamentos',
            name='nombre',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]