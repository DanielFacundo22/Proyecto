# Generated by Django 5.1 on 2024-11-02 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0014_auditoriaempleado'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='precio_costo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Precio de costo'),
        ),
    ]
