# Generated by Django 4.1.7 on 2023-04-09 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myclub', '0002_rename_attends_event_attendees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='phone',
            field=models.CharField(
                blank=True, max_length=15, verbose_name='Contact Phone'),
        ),
    ]
