# Generated by Django 5.2.1 on 2025-05-18 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_userprofile_native_language"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="purpose",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="show_purpose",
        ),
    ]
