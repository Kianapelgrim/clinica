# Generated by Django 5.0.3 on 2024-03-14 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_medicamentos_ingredientes'),
    ]

    operations = [
        migrations.CreateModel(
            name='ECMedicamentos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=255)),
            ],
        ),
    ]
