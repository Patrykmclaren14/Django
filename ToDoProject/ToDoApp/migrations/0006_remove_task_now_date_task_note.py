# Generated by Django 4.1.7 on 2023-05-18 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoApp', '0005_task_steps_alter_task_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='now_date',
        ),
        migrations.AddField(
            model_name='task',
            name='note',
            field=models.TextField(default='', max_length=50),
        ),
    ]
