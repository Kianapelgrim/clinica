# Generated by Django 5.0.3 on 2024-03-23 02:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_remove_compramedicamento_medicamento_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='compramedicamento',
            name='stock',
        ),
    ]
