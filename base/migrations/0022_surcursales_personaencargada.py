# Generated by Django 5.0.3 on 2024-03-24 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0021_documento'),
    ]

    operations = [
        migrations.AddField(
            model_name='surcursales',
            name='personaEncargada',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
