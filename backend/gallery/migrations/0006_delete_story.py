# Generated by Django 5.0.7 on 2024-08-04 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0005_alter_memory_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Story',
        ),
    ]