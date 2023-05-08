# Generated by Django 4.2.1 on 2023-05-05 21:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('property', '0005_alter_property_company_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('id',), 'verbose_name': 'Comentario', 'verbose_name_plural': 'Comentarios'},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'ordering': ('-id',), 'verbose_name': 'Inmueble', 'verbose_name_plural': 'Inmuebles'},
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
