# Generated by Django 5.0.3 on 2024-04-16 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0048_remove_preciohmedicamento_medicamento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preciohmedicamento',
            name='fechaFinal',
        ),
    ]