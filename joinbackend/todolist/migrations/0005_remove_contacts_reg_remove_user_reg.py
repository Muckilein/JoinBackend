# Generated by Django 5.0.1 on 2024-03-16 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0004_alter_user_managers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contacts',
            name='reg',
        ),
        migrations.RemoveField(
            model_name='user',
            name='reg',
        ),
    ]
