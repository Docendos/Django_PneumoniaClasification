# Generated by Django 4.2.1 on 2023-05-08 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0002_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='modile',
            new_name='mobile',
        ),
    ]
