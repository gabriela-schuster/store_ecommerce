# Generated by Django 4.0.2 on 2022-02-15 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0002_rename_state_perfil_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfil',
            name='data_aniversario',
        ),
    ]
