# Generated by Django 5.1.5 on 2025-02-20 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registry', '0002_remove_person_created_timestamp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='phonenumber',
            name='title',
        ),
    ]
