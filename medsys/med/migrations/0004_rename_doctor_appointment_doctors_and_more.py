# Generated by Django 4.2.1 on 2023-05-09 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0003_rename_modile_doctor_mobile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='doctor',
            new_name='doctors',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='patient',
            new_name='patients',
        ),
    ]