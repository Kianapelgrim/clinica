# Generated by Django 5.0.3 on 2024-04-27 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0071_alter_parametros_cai'),
    ]

    operations = [
        migrations.AddField(
            model_name='parametros',
            name='next_invoice_number',
            field=models.IntegerField(default=0),
        ),
    ]
