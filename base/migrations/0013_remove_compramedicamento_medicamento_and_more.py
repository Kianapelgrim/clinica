# Generated by Django 5.0.3 on 2024-03-23 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_detallepedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compramedicamento',
            name='medicamento',
        ),
        migrations.RemoveField(
            model_name='compramedicamento',
            name='precio',
        ),
    ]