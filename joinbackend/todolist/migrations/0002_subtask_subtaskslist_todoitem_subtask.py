# Generated by Django 5.0.1 on 2024-02-09 12:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subtask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked', models.BooleanField(default=False)),
                ('title', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SubtasksList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subtask', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.subtask')),
                ('todoitem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todolist.todoitem')),
            ],
        ),
        migrations.AddField(
            model_name='todoitem',
            name='subtask',
            field=models.ManyToManyField(through='todolist.SubtasksList', to='todolist.subtask'),
        ),
    ]
