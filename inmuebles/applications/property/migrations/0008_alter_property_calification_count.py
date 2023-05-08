# Generated by Django 4.2.1 on 2023-05-08 14:01

from django.db import migrations, models
import django.db.models.aggregates


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_property_calification_avg_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='calification_count',
            field=models.IntegerField(default=django.db.models.aggregates.Count('comments_list'), verbose_name='Cantidad de Calificaciones'),
        ),
    ]
