# Generated by Django 4.0.2 on 2022-02-15 21:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='perfil',
            old_name='state',
            new_name='estado',
        ),
    ]
