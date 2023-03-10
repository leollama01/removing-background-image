# Generated by Django 4.1 on 2023-01-21 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('handle_image', '0002_logerror'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageuploaded',
            options={'ordering': ('id',), 'verbose_name': 'Image Uploaded', 'verbose_name_plural': 'Images Uploaded'},
        ),
        migrations.AlterModelOptions(
            name='logerror',
            options={'ordering': ('id',), 'verbose_name': 'Log Error', 'verbose_name_plural': 'Log Errors'},
        ),
        migrations.AlterModelTable(
            name='imageuploaded',
            table='image_uploaded',
        ),
        migrations.AlterModelTable(
            name='logerror',
            table='log_error',
        ),
    ]
