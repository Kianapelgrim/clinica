# Generated by Django 5.0.3 on 2024-04-12 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0029_pacientes'),
    ]

    operations = [
        migrations.AddField(
            model_name='pacientes',
            name='fechaDeNacimiento',
            field=models.DateField(null=True),
        ),
    ]