# Generated by Django 4.1.7 on 2023-05-18 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoApp', '0007_step_delete_steps_alter_task_steps'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='steps',
        ),
        migrations.AddField(
            model_name='step',
            name='task',
            field=models.ManyToManyField(to='ToDoApp.task'),
        ),
    ]
