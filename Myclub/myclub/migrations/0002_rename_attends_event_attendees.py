# Generated by Django 4.1.7 on 2023-04-09 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myclub', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='attends',
            new_name='attendees',
        ),
    ]
