# Generated by Django 4.2.1 on 2023-05-09 22:27

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('website', models.URLField(max_length=250, verbose_name='Sitio de Internet')),
                ('active', models.BooleanField(default=True, verbose_name='activo')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Dirección')),
                ('country', models.CharField(max_length=50, verbose_name='País')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media', verbose_name='Imagen')),
                ('calification_avg', models.FloatField(default=0, verbose_name='Promedio de Calificaciones')),
                ('calification_count', models.IntegerField(default=0, verbose_name='Cantidad de Calificaciones')),
                ('calification_sum', models.PositiveIntegerField(default=0, verbose_name='Suma de Calificaciones')),
                ('active', models.BooleanField(default=True, verbose_name='activo')),
                ('description', models.TextField(verbose_name='Descripción')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_list', to='property.company')),
            ],
            options={
                'verbose_name': 'Inmueble',
                'verbose_name_plural': 'Inmuebles',
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calification', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, max_length=200, null=True, verbose_name='Comentario')),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('comment_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_list', to='property.property')),
            ],
            options={
                'verbose_name': 'Comentario',
                'verbose_name_plural': 'Comentarios',
                'ordering': ('id',),
            },
        ),
    ]
